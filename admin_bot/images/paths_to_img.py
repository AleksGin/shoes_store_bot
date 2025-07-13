import os


IMG_PATH = os.getenv("ADMIN_IMAGE_CONFIG__PATH")




class AdminBotImgs:
    
    welcome_img: str = f"{IMG_PATH}/admin_panel.jpg"