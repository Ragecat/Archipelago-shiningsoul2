from typing import TYPE_CHECKING
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .Locations import SS2_CLEAR_FLAGS, SS2_LOCATION_TABLE
from .Items import SS2_UNLOCK_FLAGS, SS2_ITEM_TABLE

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class ShiningSoul2Client(BizHawkClient):
    game = "Shining Soul 2"
    system = "GBA"

    ROM_HEADER_PREFIX = "SHININGSOUL2"
    local_checked_locations = set()
    local_items_received = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            header_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x080000A0, 16, "System Bus")])
            header = header_bytes[0].decode("ascii", errors="ignore")
            if not header.startswith(self.ROM_HEADER_PREFIX):
                return False
        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # Receive items from other players
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    #async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        #try:
            #await bizhawk.read(ctx.bizhawk_ctx, [(0x08FFF400, 32, "System Bus")])
        #except Exception:
            #pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed:
            return

        try:
            # Debug: Print received items count
            if len(ctx.items_received) != self.local_items_received:
                print(f"[SS2] Received {len(ctx.items_received)} items (was {self.local_items_received})")
                self.local_items_received = len(ctx.items_received)
            await self.handle_received_items(ctx)
            await self.check_locations(ctx)
                
        except bizhawk.RequestFailedError:
            pass

    async def handle_received_items(self, ctx: "BizHawkClientContext") -> None:
        if not hasattr(ctx, "items_received_index"):
            ctx.items_received_index = 0
        
        if ctx.items_received_index >= len(ctx.items_received):
            return

        id_to_name = {item_id: item_name for item_name, item_id in SS2_ITEM_TABLE.items()}

        for index in range(ctx.items_received_index, len(ctx.items_received)):
            ap_item = ctx.items_received[index]
            item_id = ap_item.item
            item_name = id_to_name.get(item_id)

            print(f"[SS2] Processing item {index + 1}/{len(ctx.items_received)}: ID={item_id}, Name={item_name}")

            if item_name is None:
                print(f"[SS2] Unknown item ID {item_id}, skipping")
                continue

            if item_name not in SS2_UNLOCK_FLAGS:
                print(f"[SS2] Item {item_name} not in SS2_UNLOCK_FLAGS, skipping")
                continue

            addr, bit = SS2_UNLOCK_FLAGS[item_name]
            mask = 1 << bit
            
            print(f"[SS2] Setting bit {bit} at address 0x{addr:08X} (mask: 0x{mask:02X})")
            
            try:
                current_value = (await bizhawk.read(ctx.bizhawk_ctx, [(addr, 1, "System Bus")]))[0][0]
                print(f"[SS2] Current value at 0x{addr:08X}: 0x{current_value:02X}")
                
                new_value = current_value | mask
                print(f"[SS2] Writing new value: 0x{new_value:02X}")
                
                await bizhawk.write(ctx.bizhawk_ctx, [(addr, [new_value], "System Bus")])
                
                verify_value = (await bizhawk.read(ctx.bizhawk_ctx, [(addr, 1, "System Bus")]))[0][0]
                print(f"[SS2] Verified value after write: 0x{verify_value:02X}")
                
                if verify_value & mask:
                    print(f"[SS2] Successfully set bit {bit} for {item_name}")
                else:
                    print(f"[SS2] WARNING: Bit {bit} was not set after write! Game may have overwritten it.")
                    
            except bizhawk.RequestFailedError:
                print(f"[SS2] Failed to write item {item_name}, will retry")
                return

        ctx.items_received_index = len(ctx.items_received)
        print(f"[SS2] Finished processing items, index now at {ctx.items_received_index}")

    async def check_locations(self, ctx: "BizHawkClientContext") -> None:
        new_checks = []

        for loc_name, (addr, bit) in SS2_CLEAR_FLAGS.items():
            if loc_name in self.local_checked_locations:
                continue

            mask = 1 << bit
            
            try:
                value = (await bizhawk.read(ctx.bizhawk_ctx, [(addr, 1, "System Bus")]))[0][0]
            except bizhawk.RequestFailedError:
                # If read fails, skip this iteration
                return
            
            if value & mask:
                loc_id = SS2_LOCATION_TABLE.get(loc_name)
                if loc_id:
                    new_checks.append(loc_id)
                    self.local_checked_locations.add(loc_name)
                    print(f"[SS2] Location checked: {loc_name}")

        if new_checks:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": new_checks
            }])
            
        if "Kill Chaos" in self.local_checked_locations and not ctx.finished_game:
            print("[SS2] Game completed!")
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])