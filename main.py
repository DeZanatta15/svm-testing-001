import streamlit as st
import utils_fr as Utils
import os

class main:
    def __init__(self):
        """
    
        """
        self.modelo = Utils.Modelo()
        self.camera = Utils.Web_cam()
        
#################/ USAGE OF DEBUGING /#############################
if __name__ == '__main__':
    modelo = main()
    web_cam = main()