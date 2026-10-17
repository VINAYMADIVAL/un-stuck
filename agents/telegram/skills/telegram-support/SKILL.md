---
name: telegram-support
description: Guide users step by step through Telegram settings and common problems (passcode lock, two-step verification password, active sessions, hiding phone number, secret chats, username, notifications). Use when the user is on Telegram and stuck.
version: 1.0.0
platform: telegram
last_verified: DRAFT-verify-before-demo
official_help: https://telegram.org/faq
---

# Telegram Support Skill

> STATUS: draft task pack. Menu labels change between app versions. Before the demo, verify each task against
> the official FAQ and set `last_verified` to the date you checked (YYYY-MM-DD).

## How to use this skill
Follow the Unstuck loop in your SOUL.md. Pick the matching task. Ask the device first for tasks marked `device: differs`.

## Platform facts
- Most settings live under **Settings** then **"Privacy and Security"**. Opening Settings: Android: tap the three-line
  menu at the top left, then "Settings". iPhone: "Settings" tab at the bottom right. Desktop: menu, then "Settings".
- Telegram has two different protections that people mix up:
  - **Passcode Lock**: protects the app on this device.
  - **Two-Step Verification**: a cloud password protecting the account when logging in on a new device.
- Telegram login codes arrive inside Telegram or by SMS. Never share them.

---

## TASK: tg-passcode-lock
**Goal:** Require a passcode (and optionally biometrics) to open Telegram on this device.
**device:** differs
**Steps**
1. Open Settings, then "Privacy and Security".
2. Tap "Passcode Lock" and turn it on.
3. The user picks a passcode and confirms it. (Do NOT ask them to tell you.)
4. Choose "Auto-Lock" time, and optionally enable fingerprint / face unlock.
**Success check:** closing and reopening Telegram asks for the passcode.
**If it doesn't work:** forgotten passcode on this device means logging out and back in (chats stay in the cloud, but secret chats on that device are lost). Warn before suggesting this.
**Source:** https://telegram.org/faq

## TASK: tg-two-step
**Goal:** Add an extra password so nobody can take over the account with just the SMS code.
**Steps**
1. Settings, then "Privacy and Security", then "Two-Step Verification".
2. Tap "Set Password" (or "Set Additional Password").
3. The user chooses a password, confirms it, adds an optional hint.
4. Add a recovery email and enter the code Telegram sends to that email (in the user's own inbox).
**Success check:** the screen shows options to change or turn off the password.
**If it doesn't work**
- Forgot the password: use "Forgot password?" on the login screen; it needs the recovery email. Without it, the official route is a waiting period. Point to the FAQ and do not promise a shortcut.
**Safety:** if someone else asked the user to set or reveal this password: scam (SOUL A5.3).
**Source:** https://telegram.org/faq (search "two-step verification")

## TASK: tg-active-sessions
**Goal:** See where the account is logged in and remove unknown devices.
**Steps**
1. Settings, then "Devices" (older versions: "Privacy and Security", then "Active Sessions").
2. Review the list. Tap an unknown device, then "Terminate Session".
3. For all others at once: "Terminate All Other Sessions".
**Success check:** only the user's own devices remain.
**Follow-up:** if anything looked unfamiliar, offer tg-two-step.
**Source:** https://telegram.org/faq (search "active sessions")

## TASK: tg-hide-phone
**Goal:** Stop people from seeing the user's phone number.
**Steps**
1. Settings, then "Privacy and Security", then "Phone Number".
2. Under "Who can see my phone number?" choose "Nobody" or "My Contacts".
3. Optionally set "Who can find me by my number?".
**Success check:** the chosen option shows next to "Phone Number".
**Note:** to be found by others without a number, the user needs a username (task tg-username).
**Source:** https://telegram.org/faq (search "phone number privacy")

## TASK: tg-username
**Goal:** Create or change a public @username.
**Steps**
1. Settings, then tap "Username" (or "Edit Profile" then "Username").
2. Type a name (letters, numbers, underscores; minimum length applies).
3. A green message means it is free. Tap "Save" or the check mark.
**If it doesn't work:** "username is already taken" or "invalid" means try another. Do not suggest paid or marketplace usernames.
**Source:** https://telegram.org/faq (search "username")

## TASK: tg-secret-chat
**Goal:** Start an end-to-end encrypted chat that only exists on the two devices.
**Steps**
1. Open the contact's profile (or the new-message screen).
2. Android: three dots, "Start Secret Chat". iPhone: tap the name, "More", "Start Secret Chat". Desktop (mobile only feature on some versions): say so honestly.
3. Confirm.
**Note:** secret chats are device-specific, do not sync across devices, and are not available in groups. Regular chats are cloud chats, not end-to-end encrypted by default.
**Source:** https://telegram.org/faq (search "secret chats")

## TASK: tg-notifications
**Goal:** Mute a noisy chat or group, or fix missing notifications.
**Steps (mute)**
1. Open the chat, tap its name at the top, tap "Mute" (choose a duration or "Mute forever").
**Steps (missing notifications)**
1. Settings, then "Notifications and Sounds": check that "Message Notifications" is on.
2. Check phone settings: notifications allowed for Telegram, battery optimization not restricting it (Android), Focus / Do Not Disturb not blocking it (iPhone).
**Source:** https://telegram.org/faq (search "notifications")

---

## Common confusions
- "I forgot my passcode" vs "I forgot my two-step password": different problems, different recovery. Ask which.
- "I'm getting login codes I didn't request": someone may be trying to log in. Do not share the code. Set two-step verification and check active sessions.

## Memory hints (for your own memory file)
Record: version-specific menu names, which branch fixed a failure, better clarifying questions. No user data.

## Change log
- 1.0.0 initial draft (unverified).
