from telethon import events
import asyncio

def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/broadcast(?:\s+(.*))?$"))
    async def broadcast_command(event):
        # Get text after command
        query = event.pattern_match.group(1)

        # If nothing provided
        if not query:
            return await event.reply(
                "**📢 Broadcast Usage:**\n\n"
                "`/broadcast user_ids`\n\n"
                "**Example:**\n"
                "`/broadcast 123456,789012,345678`\n\n"
                "**Note:** Reply to a message to broadcast it to the users!"
            )

        # Check if replying to a message
        if not event.is_reply:
            return await event.reply(
                "❌ Please reply to a message you want to broadcast!\n\n"
                "**Usage:**\n"
                "1. Reply to any message\n"
                "2. Type: `/broadcast 123456,789012`"
            )

        try:
            # Parse user IDs
            user_ids = [uid.strip() for uid in query.split(',') if uid.strip()]
            
            if not user_ids:
                return await event.reply("❌ No valid user IDs provided!")

            # Get the message to broadcast
            reply_msg = await event.get_reply_message()
            
            # Send initial status
            status_msg = await event.reply(
                f"📢 **Broadcasting...**\n"
                f"👥 Total users: {len(user_ids)}\n"
                f"⏳ Please wait..."
            )

            success_count = 0
            failed_count = 0
            failed_ids = []

            # Broadcast to each user
            for user_id in user_ids:
                try:
                    await bot.send_message(int(user_id), reply_msg)
                    success_count += 1
                    await asyncio.sleep(0.5)  # Delay to avoid flood
                except Exception as e:
                    failed_count += 1
                    failed_ids.append(f"{user_id} ({str(e)[:30]})")
                    await asyncio.sleep(0.3)

            # Final report
            report = f"✅ **Broadcast Complete!**\n\n"
            report += f"📊 **Statistics:**\n"
            report += f"✅ Success: {success_count}\n"
            report += f"❌ Failed: {failed_count}\n"
            report += f"📋 Total: {len(user_ids)}\n"

            if failed_ids:
                report += f"\n**Failed IDs:**\n"
                for fid in failed_ids[:10]:  # Show first 10 failed
                    report += f"• {fid}\n"
                if len(failed_ids) > 10:
                    report += f"... and {len(failed_ids) - 10} more"

            await status_msg.edit(report)

        except ValueError:
            await event.reply("❌ Invalid user ID format! Use numbers separated by commas.")
        except Exception as e:
            await event.reply(f"❌ Error occurred: {str(e)}")
