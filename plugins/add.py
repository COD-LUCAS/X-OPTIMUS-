from telethon import events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors import UserPrivacyRestrictedError, UserNotMutualContactError, UserChannelsTooMuchError, PeerFloodError
import asyncio

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/add(?:\s+(.*))?$"))
    async def add_command(event):
        # Check if command is used in a group
        if event.is_private:
            return await event.reply("❌ This command only works in groups!")

        # Get text after command
        query = event.pattern_match.group(1)

        # If nothing provided
        if not query:
            return await event.reply(
                "**👥 Add Users Usage:**\n\n"
                "`/add user_ids`\n\n"
                "**Example:**\n"
                "`/add 123456,789012,345678`\n\n"
                "**Note:** Works only in groups/channels!"
            )

        try:
            # Parse user IDs
            user_ids = [uid.strip() for uid in query.split(',') if uid.strip()]
            
            if not user_ids:
                return await event.reply("❌ No valid user IDs provided!")

            # Send initial status
            status_msg = await event.reply(
                f"➕ **Adding users to group...**\n"
                f"👥 Total users: {len(user_ids)}\n"
                f"⏳ Please wait..."
            )

            success_count = 0
            failed_count = 0
            failed_details = []

            # Add each user to the group
            for user_id in user_ids:
                try:
                    # Convert to integer
                    uid = int(user_id)
                    
                    # Try to add user
                    await bot(InviteToChannelRequest(
                        event.chat_id,
                        [uid]
                    ))
                    
                    success_count += 1
                    await asyncio.sleep(2)  # Important delay to avoid flood bans
                    
                except UserPrivacyRestrictedError:
                    failed_count += 1
                    failed_details.append(f"{user_id}: Privacy settings")
                except UserNotMutualContactError:
                    failed_count += 1
                    failed_details.append(f"{user_id}: Not mutual contact")
                except UserChannelsTooMuchError:
                    failed_count += 1
                    failed_details.append(f"{user_id}: Too many groups")
                except PeerFloodError:
                    failed_count += 1
                    failed_details.append(f"{user_id}: Flood wait")
                    await asyncio.sleep(5)  # Extra delay on flood
                except ValueError:
                    failed_count += 1
                    failed_details.append(f"{user_id}: Invalid ID")
                except Exception as e:
                    failed_count += 1
                    error_msg = str(e)[:40]
                    failed_details.append(f"{user_id}: {error_msg}")
                    await asyncio.sleep(1)

            # Final report
            report = f"✅ **Add Users Complete!**\n\n"
            report += f"📊 **Statistics:**\n"
            report += f"✅ Successfully added: {success_count}\n"
            report += f"❌ Failed: {failed_count}\n"
            report += f"📋 Total attempted: {len(user_ids)}\n"

            if failed_details:
                report += f"\n**❌ Failed Users:**\n"
                for detail in failed_details[:10]:  # Show first 10
                    report += f"• {detail}\n"
                if len(failed_details) > 10:
                    report += f"... and {len(failed_details) - 10} more\n"
                
                report += f"\n**💡 Tip:** Users may fail due to:\n"
                report += f"• Privacy settings\n"
                report += f"• Not being mutual contacts\n"
                report += f"• Being in too many groups\n"
                report += f"• Flood protection"

            await status_msg.edit(report)

        except ValueError:
            await event.reply("❌ Invalid user ID format! Use numbers separated by commas.")
        except Exception as e:
            await event.reply(f"❌ Error occurred: {str(e)}")
            print(f"Add users error: {e}")
