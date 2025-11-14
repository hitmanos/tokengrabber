Overview
Advanced Discord token extraction tool developed by HITMAN for security research and educational purposes. This tool scans multiple locations for Discord authentication tokens and sends detailed reports via Discord webhooks.

Features
Multi-Source Scanning: Extracts tokens from Discord desktop applications and browsers

Real-time Validation: Verifies token validity through Discord API

Encrypted Token Decryption: Decrypts protected tokens using Windows DPAPI

Rich Webhook Reports: Sends formatted embeds with user avatars and detailed information

Stealth Operation: Designed to avoid detection by security software

Supported Sources
Discord Applications
Discord

Discord Canary

Discord PTB

Discord Development

Browser Support
Google Chrome

Microsoft Edge

Brave Browser

Browser-based Discord clients

Token Types Extracted
Standard authentication tokens (24.6.27 format)

MFA-enabled tokens (mfa. format)

Encrypted local storage tokens (dQw4w9WgXcQ format)

Information Collected
Authentication tokens

Username and discriminator

Email address

Phone number (if available)

User ID

Avatar/profile picture

2FA status

Installation & Usage
Prerequisites
Windows operating system

Python 3.7+

Discord webhook URL

Setup
Configure your webhook URL in the script

Run the script - dependencies install automatically

Tokens are automatically sent to your webhook

Webhook Configuration
python
WEBHOOK_URL = "your_discord_webhook_url_here"
Technical Details
Scanning Locations
%APPDATA%\Discord\Local Storage\leveldb

%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage

Browser profile directories and Discord application data

Security Features
Automatic dependency installation

Token validation before sending

Encrypted token decryption

Webhook-based secure reporting

Legal Notice
⚠️ IMPORTANT: FOR AUTHORIZED USE ONLY

This tool is intended for:

Security research and education

Authorized penetration testing

Personal account recovery (your own accounts only)

Prohibited Uses:

Unauthorized access to systems

Account theft or hacking

Any illegal activities

Users are solely responsible for complying with applicable laws and terms of service. The developer assumes no liability for misuse.

Developer
HITMAN
GitHub: github.com/hitmanos/tokengrabber

Disclaimer
This tool is provided for educational and security research purposes only. Always ensure you have proper authorization before scanning any system. Respect privacy and follow ethical guidelines in all security testing activities.

Support
For issues and feature requests, visit the GitHub repository:
https://github.com/hitmanos/tokengrabber
my discord server https://discord.gg/CrAqFQkvHC
צאm

Last Updated: 14/11/2025
Version: 1.0
Developer: HITMAN
