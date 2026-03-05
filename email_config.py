# 邮箱配置统一文件
# 所有邮件脚本从此文件读取配置，避免硬编码分散

EMAIL_CONFIG = {
    "sender": "lunchwu@gmail.com",
    "password": "bize wlmw kupz jnoc",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "recipients": {
        "primary": "lunchwu@gmail.com",
        "cc": [
            "jerry.wu1@decathlon.com",
            "leanna.li@decathlon.com",
            "tia.song@decathlon.com"
        ]
    }
}
