---
name: discord-support
description: Guide users step by step through Discord settings and common problems (two-factor authentication, privacy and DM settings, notifications and muting, server nickname, Developer Mode, "can't see a channel" permissions). Use when the user is on Discord and stuck.
version: 1.0.0
platform: discord
last_verified: DRAFT-verify-before-demo
official_help: https://support.discord.com
---

# Discord Support Skill

> STATUS: draft task pack. Discord updates its UI often. Before the demo, verify each task against the official
> support center and set `last_verified` to the date you checked (YYYY-MM-DD).

## How to use this skill
Follow the Unstuck loop in your SOUL.md. Pick the matching task. Ask the device first for tasks marked `device: differs`.

## Platform facts
- **User Settings** = the gear icon next to the user's name at the bottom left (desktop/web). Mobile: tap the
  profile picture at the bottom right.
- **Server settings** and **channel permissions** are controlled by server admins/moderators, not by Unstuck.
- Discord support never asks for passwords, 2FA codes, or backup codes.

---

## TASK: dc-2fa
**Goal:** Turn on two-factor authentication (2FA) with an authenticator app.
**device:** differs
**Steps**
1. Open User Settings, then "My Account".
2. Find "Password and Authentication" and tap "Enable Authenticator App".
3. Enter the account password when asked (the user types it into Discord only, never to you).
4. Install an authenticator app on the phone if they don't have one, scan the QR code, and enter the 6-digit code shown in that app.
5. Download or write down the **backup codes** and keep them offline. Never share them.
**Success check:** "Authenticator App" shows as enabled, and backup codes are available.
**If it doesn't work:** code rejected usually means the phone's clock is wrong. Turn on automatic date and time, then retry.
**Source:** https://support.discord.com (search "two-factor authentication")

## TASK: dc-dm-privacy
**Goal:** Stop strangers from messaging the user or adding them.
**Steps**
1. User Settings, then "Privacy and Safety" (mobile: "Content and Social" / "Privacy and Safety" depending on version).
2. Turn off "Allow direct messages from server members" for all servers, or per server (right-click or long-press the server, then "Privacy Settings").
3. Set "Who can add you as a friend" to the needed level.
4. Under message-safety options choose the level of filtering for direct messages.
**Success check:** the toggles reflect the new choices.
**Note:** already-open DMs are not closed by this. Use "Block" on a person for that.
**Source:** https://support.discord.com (search "privacy and safety")

## TASK: dc-mute-notifications
**Goal:** Stop pings from a noisy server or channel.
**Steps**
1. Server: right-click (long-press on mobile) the server icon, then "Mute Server" and choose a duration.
2. Channel: right-click the channel, then "Mute Channel".
3. For @everyone / @here and role pings: server menu, "Notification Settings", then turn off those toggles.
**Success check:** the server or channel icon appears dimmed.
**If notifications are missing instead:** check User Settings, "Notifications", and the phone's notification and battery settings.
**Source:** https://support.discord.com (search "notification settings")

## TASK: dc-server-nickname
**Goal:** Use a different display name or avatar in one server.
**Steps**
1. Right-click (long-press) the server icon, then "Edit Server Profile" (older versions: "Change Nickname").
2. Enter the nickname, and avatar if wanted, and save.
**If it doesn't work:** the server admins may have disabled nickname changes. Ask an admin or moderator.
**Source:** https://support.discord.com (search "server profile" or "nickname")

## TASK: dc-developer-mode
**Goal:** Copy user, server, or channel IDs (needed for bots, reports, or support tickets).
**Steps**
1. User Settings, then "Advanced".
2. Turn on "Developer Mode".
3. Right-click (long-press) a user, server, or channel and choose "Copy ID".
**Safety:** an ID is not a secret like a token. But never share a bot token or account token with anyone.
**Source:** https://support.discord.com (search "Where can I find my User/Server/Message ID")

## TASK: dc-cant-see-channel
**Goal:** The user can't see a channel, can't type, or can't join voice.
**Steps (diagnose, one question at a time)**
1. Is the channel missing, or visible but locked (lock icon)? Is the message box disabled?
2. Is the user's role low in the server? Roles and channel permissions are set by admins.
3. Is the server in "Rules Screening" or "Membership Screening" waiting to be accepted?
4. For voice: check User Settings, "Voice and Video", input device, and permission for the microphone in the phone/computer settings.
**Resolution:** server permissions can only be changed by admins. Offer a short, polite message the user can send to a moderator.
**Source:** https://support.discord.com (search "permissions" or "roles")

---

## Common confusions
- "Account Settings vs Server Settings": the first affects the user everywhere; the second affects one server and may need admin rights.
- "Someone says they'll give Nitro / free items if I scan a QR code or log in": scam. Do not scan or enter anything. Discord logins via QR from strangers hijack accounts (SOUL A5.3).

## Memory hints (for your own memory file)
Record: version-specific menu names, which branch fixed a failure, better clarifying questions. No user data.

## Change log
- 1.0.0 initial draft (unverified).
