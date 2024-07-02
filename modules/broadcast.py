"""
 ^|^x **Bantuan Untuk Broadcast**

  ^o **Perintah:** `gcast`
 ^w^i **Keterangan:** Kirim pesan ke semua obrolan grup (Otomatis YA TOD).

  ^o **Perintah:** `gucast`
 ^w^i **Keterangan:** Kirim pesan ke semua pengguna pribadi.

  ^o **Perintah:** `addbl`
 ^w^i **Keterangan:** Tambahkan grup ke dalam anti gcast.

  ^o **Perintah:** `delbl`
 ^w^i **Keterangan:** Hapus grup dari daftar anti gcast.

  ^o **Perintah:** `blchat`
 ^w^i **Keterangan:** Melihat daftar anti gcast.
"""
import asyncio

from Ayra.dB import DEVS
from Ayra.dB.gcast_blacklist_db import add_gblacklist, list_bl, rem_gblacklist
from telethon.errors.rpcerrorlist import FloodWaitError

from . import *

gcast_loop = None
loop_count = 0  # Initialize loop counter

@ayra_cmd(pattern="[gG][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gcast(event):
    global gcast_loop, loop_count
    if gcast_loop is not None:
        await eor(event, "`Gcast Otomatis Sudah Jalan tod.`")
        return

    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eor(
            event, "`Berikan beberapa teks ke Globally Broadcast atau balas pesan..`"
        )

    kk = await event.eor("`Sabar ya Kalo Limit Jangan Marah bngst...`")
    er = 0
    done = 0
    err = ""
    chat_blacklist = udB.get_key("GBLACKLISTS") or []
    chat_blacklist.append(-1001608847572)
    udB.set_key("GBLACKLISTS", chat_blacklist)
    gcast_loop = asyncio.get_event_loop().create_task(send_message_loop(event, msg, kk))
    await gcast_loop

async def send_message_loop(event, msg, kk):
    global gcast_loop, loop_count

    while gcast_loop is not None:
        loop_count += 1  # Increment loop counter before starting
        er = 0
        done = 0
        err = ""
        piu = ""
        chat_blacklist = udB.get_key("GBLACKLISTS") or []
        chat_blacklist.append(-1001608847572)
        udB.set_key("GBLACKLISTS", chat_blacklist)
        async for x in event.client.iter_dialogs():
            if x.is_group:
                chat = x.id
                if chat not in chat_blacklist and chat not in NOSPAM_CHAT:
                    try:
                        await event.client.send_message(chat, msg)
                        done += 1
                    except FloodWaitError as fw:
                        await asyncio.sleep(fw.seconds + 10)
                        try:
                            await event.client.send_message(chat, msg)
                            done += 1
                        except Exception as rr:
                            err += f" ^`  {rr}\n"
                            er += 1
                    except BaseException as h:
                        err += f" ^`  {str(h)}" + "\n"
                        er += 1

        y = await eor(event,
            f"**Pesan Broadcast Berhasil Terkirim Ke : `{done}` Grup.\nDan Gagal Terkirim Ke : `{er}` Grup. Gcast ke-{loop_count}**"
        )
        await y.edit (f"Gcast ke-{loop_count}")
        await asyncio.sleep(180)  # Wait for 5 minutes before sending the next broadcast

        if gcast_loop is None:
            break

@ayra_cmd(pattern="[gG][s][t][o][p]", fullsudo=False)
async def gstop(event):
    global gcast_loop, loop_count
    ppk = await eor(event, "`Menghentikan broadcast otomatis...`")
    if gcast_loop is not None:
        gcast_loop.cancel()
        gcast_loop = None
        loop_count = 0
    await ppk.edit(f"`Broadcast Otomatis Dihentikan.`")


@ayra_cmd(pattern="[gG][u][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gucast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eor(
            event, "`Berikan beberapa teks ke Globally Broadcast atau balas pesan..`"
        )
    kk = await event.eor("`Sebentar Kalo Limit Jangan Salahin Kynan Ya...`")
    er = 0
    done = 0
    chat_blacklist = udB.get_key("GBLACKLISTS") or []
    chat_blacklist.append(482945686)
    udB.set_key("GBLACKLISTS", chat_blacklist)
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in DEVS and chat not in chat_blacklist:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**Pesan Broadcast Berhasil Terkirim Ke : `{done}` Pengguna.\nDan Gagal Terkirim Ke : `{er}` Pengguna.**"
    )


@ayra_cmd(pattern="[Aa][d][d][b][l]")
@register(incoming=True, from_users=DEVS, pattern=r"^Addbl$")
async def blacklist_(event):
    await gblacker(event, "add")

@ayra_cmd(pattern="[dD][e][l][b][l]")
async def ungblacker(event):
    await gblacker(event, "remove")


@ayra_cmd(pattern="[Bb][l][c][h][a][t]")
async def chatbl(event):
    id = event.chat_id
    if xx := list_bl(id):
        sd = "** ^`  Daftar Blacklist Gcast**\n\n"
        return await event.eor(sd + xx)
    await event.eor("**Belum ada daftar**")


async def gblacker(event, type_):
    args = event.text.split()
    if len(args) > 2:
        return await event.eor("**Gunakan Format:**\n `delbl` or `addbl`")
    chat_id = None
    chat_id = int(args[1]) if len(args) == 2 else event.chat_id
    if type_ == "add":
        add_gblacklist(chat_id)
        await event.eor(f"**Ditambahkan ke dalam Blacklist Gcast**\n`{chat_id}`")
    elif type_ == "remove":
        rem_gblacklist(chat_id)
        await event.eor(f"**Dihapus dari Blacklist Gcast**\n`{chat_id}`")
