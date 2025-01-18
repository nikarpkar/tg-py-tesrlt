import aiohttp
import asyncio
import os, time
from pyrogram import Client, filters



async def download_file(url, download_path, message):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(download_path, "wb") as file:
                total = int(response.headers['Content-Length'])
                current = 0
                start_time = time.time()
                last_update_time = time.time()
                while True:
                    chunk = await response.content.read(1024)  # Read in chunks
                    if not chunk:
                        break  # Exit when file is fully downloaded
                    file.write(chunk)
                    current += len(chunk)

                    # Update progress every 10 seconds
                    elapsed_time = time.time() - start_time
                    speed = current / elapsed_time if elapsed_time > 0 else 0
                    if time.time() - last_update_time >= 10:
                        last_update_time = time.time()
                        await update_progress_message(message, current, total, speed)

async def update_progress_message(message, current, total, speed):
    percentage = (current / total) * 100
    speed_str = f"{speed / 1024:.2f} KB/s"  # Convert speed to KB/s
    progress_text = f"Download Progress: {percentage:.2f}% - Speed: {speed_str}"
    
    # Update the same message (avoid sending new messages)
    await message.edit_text(progress_text)

async def upload_file(client, file_path, chat_id, message):
    with open(file_path, "rb") as f:
        # Send the file using pyrogram's send_document and show progress
        await client.send_document(
            chat_id=chat_id,
            document=f,
            caption="Uploading file...",
            progress=progress_callback,
            progress_args=(message,)
        )

async def progress_callback(current, total, message):
    percentage = (current / total) * 100
    speed = current / (time.time() - start_time) if time.time() - start_time > 0 else 0
    await update_progress_message(message, current, total, speed)

async def process_file(client, chat_id, url, download_path, message):
    # Step 1: Download the file
    await download_file(url, download_path, message)

    # Step 2: Upload the file once it's downloaded
    await upload_file(client, download_path, chat_id, message)

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    # Replace with the actual file URL you want to download
    url="https://rs16.seedr.cc/ff_get/5584167991/brazzersexxtra.25.01.17.lulu.chu.and.vanessa.marie.knob.slobbing.the.peeper.480p.mp4?st=RyxhesQu-6-YWq1CBFOchg&e=1737265455"
    download_path = "downloaded_file.mp4"  # Path where the file will be saved

    # Start the download and upload process
    await message.reply("Starting download and upload...")
    await process_file(client, message.chat.id, url, download_path, message)
    await message.reply("File upload complete!")


