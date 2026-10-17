---
name: whatsapp-support
description: Guide users step by step through WhatsApp settings and common problems (two-step verification PIN, chat lock, screen lock, privacy, disappearing messages, linked devices). Use when the user is on WhatsApp and stuck.
version: 1.0.0
platform: whatsapp
last_verified: DRAFT-verify-before-demo
official_help: https://faq.whatsapp.com
---

# WhatsApp Support Skill

> STATUS: draft task pack. Menu labels change between app versions. Before the demo, verify each task against
> the official help center and set `last_verified` to the date you checked (YYYY-MM-DD).

## How to use this skill
Follow the Unstuck loop in your SOUL.md (CLARIFY, LOCATE, GUIDE, CONFIRM, RECOVER, CLOSE, LEARN).
Pick the task below that matches the goal. Give one step at a time. Ask Android or iPhone first for
tasks marked `device: differs`.

## Platform facts
- Android: settings via the **three dots** at the top right of the Chats screen, then "Settings".
- iPhone: the **"Settings"** tab at the bottom right.
- Two-step verification PIN is **6 digits**, chosen by the user. WhatsApp will never ask for it by SMS or call.
- The 6-digit SMS **registration code** is different from the PIN. Never share either.

---

## TASK: wa-two-step-pin
**Goal:** Turn on two-step verification (set a 6-digit PIN) to protect the account.
**device:** differs
**Steps**
1. Android: tap the three dots, then "Settings". iPhone: tap the "Settings" tab.
2. Tap "Account".
3. Tap "Two-step verification", then "Turn on" (or "Enable").
4. The user chooses a 6-digit PIN and enters it, then confirms it. (Do NOT ask them to tell you the PIN.)
5. Offer to add an email address (recommended: it is the only way to reset a forgotten PIN). Tap "Next", enter email, confirm.
6. Tap "Done" or "Save".
**Success check:** "Two-step verification" now shows turn-off / change-PIN options.
**If it doesn't work**
- No "Two-step verification" under "Account": update WhatsApp, then look again.
- Forgot the PIN: tap "Forgot PIN?" on the PIN screen. A reset link goes to the email they added earlier.
  If no email was added, do not promise a workaround. Point to the official help page.
- Asked for a PIN by someone else: scam (see SOUL A5.3).
**Source:** https://faq.whatsapp.com (search "two-step verification")

## TASK: wa-chat-lock
**Goal:** Lock a private chat behind fingerprint, face, or phone passcode.
**device:** differs
**Steps**
1. Open the chat.
2. Tap the contact or group name at the top.
3. Scroll to "Chat lock" and tap it.
4. Turn on "Lock this chat with fingerprint" (iPhone: Face ID / Touch ID wording).
5. Confirm with fingerprint, face, or passcode.
**Success check:** the chat disappears from the main list into the "Locked chats" folder (pull down the chat list / scroll to top to find it).
**If it doesn't work**
- Option missing: update WhatsApp; the phone must have a screen lock set up.
**Source:** https://faq.whatsapp.com (search "chat lock")

## TASK: wa-screen-lock
**Goal:** Require fingerprint/face to open the whole app.
**device:** differs
**Steps**
1. Android: three dots, "Settings", "Privacy". iPhone: "Settings" tab, "Privacy".
2. Scroll down. Android: "App lock". iPhone: "Screen Lock".
3. Turn it on and choose when to require unlock (immediately / after a delay).
**Success check:** reopening WhatsApp asks for fingerprint, face, or passcode.
**If it doesn't work:** the phone needs a screen lock and biometrics enrolled in phone settings.
**Source:** https://faq.whatsapp.com (search "screen lock" or "app lock")

## TASK: wa-privacy-last-seen
**Goal:** Hide or limit who sees "last seen", profile photo, or "online".
**Steps**
1. Open Settings (see Platform facts), then "Privacy".
2. Tap "Last seen and online" (or "Last Seen").
3. Choose "Everyone", "My contacts", "My contacts except…", or "Nobody".
4. Repeat for "Profile photo" and "About" if wanted.
**Success check:** the chosen option is shown next to the setting.
**Note:** hiding last seen also hides other people's last seen from the user on some versions. Tell them.
**Source:** https://faq.whatsapp.com (search "privacy settings")

## TASK: wa-disappearing-messages
**Goal:** Make messages in a chat vanish after 24 hours, 7 days, or 90 days.
**Steps**
1. Open the chat, tap the name at the top.
2. Tap "Disappearing messages".
3. Pick a duration.
**Success check:** a notice appears in the chat saying disappearing messages are on.
**Note:** applies to new messages only. A recipient can still screenshot or forward.
**Source:** https://faq.whatsapp.com (search "disappearing messages")

## TASK: wa-linked-devices
**Goal:** Check or remove devices (WhatsApp Web, Desktop) that are logged in, e.g. after a lost laptop or a suspicious login.
**Steps**
1. Android: three dots, then "Linked devices". iPhone: "Settings", then "Linked devices".
2. Review the list. Unknown device? Tap it, then "Log out".
**Success check:** the device is no longer listed.
**Safety:** if the user sees a device they don't recognize, advise turning on two-step verification (task wa-two-step-pin).
**Source:** https://faq.whatsapp.com (search "linked devices")

---

## Common confusions
- "Where is Settings?" Android: three dots top right. iPhone: bottom-right tab.
- "I got a code by SMS I didn't ask for": someone may be trying to register their number. Do not share it. Turn on two-step verification.
- "Will I lose my chats?" Changing settings does not delete chats. Re-installing without a backup can. Say which.

## Memory hints (for your own memory file)
Record: menu label changes by version, which branch fixed a failure, better clarifying questions.
Do not record: any user data.

## Change log
- 1.0.0 initial draft (unverified).
