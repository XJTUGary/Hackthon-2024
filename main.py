import streamlit as st
from streamlit_option_menu import option_menu
from tools.utilities import load_css
from views.dashboard import Dashboard
from views.data_inference import DataInference
from views.data_review import DataReview
from views.chat import Chat
import streamlit_javascript as st_js

st.set_page_config(
    page_title="LikeIDo",
    page_icon="favicon.ico",
    layout="wide"
)

load_css()


class Model:
    menuTitle = "LikeIDo"
    option1 = "Invoice Extraction"
    option2 = "Data Review"
    option3 = "Dashboard"
    option4 = "Chat"

    menuIcon = "menu-up"
    icon1 = "journal-arrow-down"
    icon2 = "droplet"
    icon3 = "speedometer"
    icon4 = "chat"


def view(model):
    with st.sidebar:
        menuItem = option_menu(model.menuTitle,
                               [model.option1, model.option2, model.option3, model.option4],
                               icons=[model.icon1, model.icon2, model.icon3, model.icon4],
                               menu_icon=model.menuIcon,
                               default_index=0,
                               styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#037ffc"},
                               })
        st.sidebar.empty()

    if menuItem == model.option1:
        if 'ui_width' not in st.session_state or 'device_type' not in st.session_state or 'device_width' not in st.session_state:
            # Get UI width
            ui_width = st_js.st_javascript("window.innerWidth", key="ui_width_comp")
            device_width = st_js.st_javascript("window.screen.width", key="device_width_comp")

            if ui_width > 0 and device_width > 0:
                # Add 20% of current screen width to compensate for the sidebar
                ui_width = round(ui_width + (20 * ui_width / 100))

                if device_width > 768:
                    device_type = 'desktop'
                else:
                    device_type = 'mobile'

                st.session_state['ui_width'] = ui_width
                st.session_state['device_type'] = device_type
                st.session_state['device_width'] = device_width

                st.experimental_rerun()
        else:
            DataInference().view(DataInference.Model(), st.session_state['ui_width'], st.session_state['device_type'],
                                 st.session_state['device_width'])

        logout_widget()

    if menuItem == model.option2:
        if 'ui_width' not in st.session_state or 'device_type' not in st.session_state or 'device_width' not in st.session_state:
            # Get UI width
            ui_width = st_js.st_javascript("window.innerWidth", key="ui_width_comp")
            device_width = st_js.st_javascript("window.screen.width", key="device_width_comp")

            if ui_width > 0 and device_width > 0:
                # Add 20% of current screen width to compensate for the sidebar
                ui_width = round(ui_width + (20 * ui_width / 100))

                if device_width > 768:
                    device_type = 'desktop'
                else:
                    device_type = 'mobile'

                st.session_state['ui_width'] = ui_width
                st.session_state['device_type'] = device_type
                st.session_state['device_width'] = device_width

                st.experimental_rerun()
        else:
            DataReview().view(DataReview.Model(), st.session_state['ui_width'], st.session_state['device_type'],
                              st.session_state['device_width'])

        logout_widget()

    if menuItem == model.option3:
        Dashboard().view(Dashboard.Model())
        logout_widget()

    if menuItem == model.option4:
        Chat().view(Chat.Model())
        logout_widget()


def logout_widget():
    with st.sidebar:
        st.markdown("---")
        st.write("Version:", "1.0.0")
        st.write("©️ 2024 Markets GenAI Hackathon")


view(Model())
