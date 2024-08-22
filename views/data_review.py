import streamlit as st
from natsort import natsorted
import os
from PIL import Image
import math
from streamlit_sparrow_labeling import st_sparrow_labeling
import json
import pandas as pd
from glob import glob



class DataReview:
    class Model:
        # pageTitle = "Data Review"
        subheader_2 = "Select"
        subheader_3 = "Result"
        selection_text = "File to review"
        initial_msg = "Please select a file to review"

        img_file = None

        def set_image_file(self, img_file):
            st.session_state['img_file_review'] = img_file

        def get_image_file(self):
            if 'img_file_review' not in st.session_state:
                return None
            return st.session_state['img_file_review']

        json_file = None

        def set_json_file(self, json_file):
            st.session_state['json_file_review'] = json_file

        def get_json_file(self):
            if 'json_file_review' not in st.session_state:
                return None
            return st.session_state['json_file_review']

    def view(self, model, ui_width, device_type, device_width):
        data = [
            {
                "INVOICE NO": "40378170",
                "INVOICE DATE": "10/15/2012",
                "TYPE": "Transportation",
                "SELLER": "Patel, Thompson and Montgomery 356 Kyle Vista New James, MA 46228",
                "CLIENT": "Jackson, Odonnell and Jackson 267 John Track Suite 841 Jenniferville, PA 98601",
                "TOTAL GROSS WORTH": "$8,25",
                "FILE NAME": "invoice_0_168236533145547"
            },
            {
                "INVOICE NO": "31447231",
                "INVOICE DATE": "06/18/2017",
                "TYPE": "Food",
                "SELLER": "Sellers, Marsh and Cabrera 54819 Laura Hollow Suite 093 Port Jenniferstad, FL 48593",
                "CLIENT": "English-Sanchez 682 Kimberly Plain Apt. 213 Adamport, DE 94746",
                "TOTAL GROSS WORTH": "$8357,28",
                "FILE NAME": "invoice_583_1683791077281225"
            },
            {
                "INVOICE NO": "99935945",
                "INVOICE DATE": "03/19/2014",
                "TYPE": "Transportation",
                "SELLER": "Fox-Reeves 83481 Tracy Neck Lake Eddieburgh, LA 08023",
                "CLIENT": "Myers PLC 80956 Bob Mission Michelleside, DC 87406",
                "TOTAL GROSS WORTH": "$1349,08",
                "FILE NAME": "invoice_587_1683791244407337"
            }
        ]

        ## Create DataFrame
        df = pd.DataFrame(data)
        df['issue_date'] = pd.to_datetime(df['issue_date'])

        # Add custom CSS for the label
        st.markdown("""
        <style>
        .custom-label {
            font-size: 24px; /* Adjust the size as needed */
            font-weight: bold;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)



        with st.form("search"):
            col1, col2, col3 = st.columns([5,1,1])
            with col1:
                search_term = st.text_input("Keywords: ", placeholder="Type to search...")
            with col2:
                order_by = st.selectbox(label="Order by:", options=df.columns)
            with col3:
                order = st.selectbox(label="ASC/DESC", options=["ASC", "DESC"])

            with st.expander("Advanced search query"):
                invoice_types = df['invoice_type'].unique()
                min_date = pd.to_datetime("2000-10-01")
                max_date = pd.to_datetime("2025-10-01")
                col1, col2 = st.columns(2)
                with col1:
                    type_multiselect = st.multiselect("Select Invoice Types:", options=invoice_types)
                with col2:
                    date_range = st.date_input("Invoice Date Range:", (min_date, max_date))

                invoice_status = st.radio(
                    "Invoice Status:",
                    options=["All", "Valid", "Invalid"]
                )
                total_range = st.slider(label="Total pay:", min_value=0.0, max_value=99999.0, step=10.0, value=(0.0, 10000.0))

            submit_button = st.form_submit_button(label="Search")

        if submit_button:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

            if type_multiselect:
                filtered_df = filtered_df[filtered_df['invoice_type'].isin(type_multiselect)]

            start_date, end_date = date_range
            filtered_df = filtered_df[(filtered_df['issue_date'] >= pd.to_datetime(start_date)) &
                                      (filtered_df['issue_date'] <= pd.to_datetime(end_date))]

            # Apply sorting
            if order_by in filtered_df.columns:
                ascending = True if order == "ASC" else False
                filtered_df = filtered_df.sort_values(by=order_by, ascending=ascending)
        else:
            filtered_df = df


        # Search functionality
        st.markdown("<br>", unsafe_allow_html=True)  # Add a line break for spacing

        # Function to apply row-based styling
        def highlight_exceptions(row):
            return ['background-color: #f8d7da' if row["Exception"] == "Yes" else '' for _ in row]

        # # Display DataFrame with styling
        # st.dataframe(
        #     filtered_df.style
        #     .apply(highlight_exceptions, axis=1)
        #     .set_properties(**{
        #         "color": "#333",
        #         "border": "1px solid #ddd"
        #     })
        #     .set_table_styles([{
        #         'selector': 'thead th',
        #         'props': [('background-color', '#037ffc'), ('color', 'white')]
        #     }]),
        #     width=ui_width if ui_width else 800,
        #     height=800
        # )
        #
        # with st.expander(f"Invoice Details for", expanded=True):
        #     selection = 'invoice_587_1683791244407337'
        #     img_file = "docs/inference/" + selection + ".jpg"
        #     json_file = "docs/inference/" + selection + ".json"
        #
        #     model.set_image_file(img_file)
        #     model.set_json_file(json_file)
        #
        #     if model.get_image_file() is not None:
        #         doc_img = Image.open(model.get_image_file())
        #         doc_height = doc_img.height
        #         doc_width = doc_img.width
        #
        #         canvas_width, number_of_columns = self.canvas_available_width(ui_width, doc_width, device_type,
        #                                                                       device_width)
        #
        #         if number_of_columns > 1:
        #             col1, col2 = st.columns([number_of_columns, 10 - number_of_columns])
        #             with col1:
        #                 pass
        #                 self.render_doc(model, doc_img, canvas_width, doc_height, doc_width)
        #             with col2:
        #                 pass
        #                 self.render_results(model)
        #         else:
        #             pass
        #             self.render_doc(model, doc_img, canvas_width, doc_height, doc_width)
        #             self.render_results(model)
        #     else:
        #         st.title(model.initial_msg)

        attributes_to_display = [
            "invoice_type", "invoice_code", "issue_date", "vendor", "customer", "city", "currency", "amount"]
        # 显示每行的标题和内容
        for i, row in filtered_df.iterrows():
            title = "\u2002|\u2002".join([f"{attr}: {row[attr]}" for attr in attributes_to_display])

            with st.expander(title, expanded=False):

                selection = row["FILE NAME"]
                img_file = "docs/inference/" + selection + ".jpg"
                json_file = "docs/inference/" + selection + ".json"

                model.set_image_file(img_file)
                model.set_json_file(json_file)

                if model.get_image_file() is not None:
                    doc_img = Image.open(model.get_image_file())
                    doc_height = doc_img.height
                    doc_width = doc_img.width

                    canvas_width, number_of_columns = self.canvas_available_width(ui_width, doc_width, device_type,
                                                                                  device_width)

                    if number_of_columns > 1:
                        col1, col2 = st.columns([number_of_columns, 10 - number_of_columns])
                        with col1:
                            self.render_doc(model, doc_img, canvas_width, doc_height, doc_width)
                        with col2:
                            self.render_results(model)
                    else:
                        self.render_doc(model, doc_img, canvas_width, doc_height, doc_width)
                        self.render_results(model)
                else:
                    st.title(model.initial_msg)


    def get_processed_file_names(self, dir_name):
        # get ordered list of files without file extension, excluding hidden files, with JSON extension only
        file_names = [os.path.splitext(f)[0] for f in os.listdir(dir_name) if
                        os.path.isfile(os.path.join(dir_name, f)) and not f.startswith('.') and f.endswith('.json')]
        file_names = natsorted(file_names)
        return file_names

    def get_selection_index(self, file, files_list):
        return files_list.index(file)

    def canvas_available_width(self, ui_width, doc_width, device_type, device_width):
        doc_width_pct = (doc_width * 100) / ui_width
        if doc_width_pct < 45:
            canvas_width_pct = 37
        elif doc_width_pct < 55:
            canvas_width_pct = 49
        else:
            canvas_width_pct = 60

        if ui_width > 700 and canvas_width_pct == 37 and device_type == "desktop":
            return math.floor(canvas_width_pct * ui_width / 100), 4
        elif ui_width > 700 and canvas_width_pct == 49 and device_type == "desktop":
            return math.floor(canvas_width_pct * ui_width / 100), 5
        elif ui_width > 700 and canvas_width_pct == 60 and device_type == "desktop":
            return math.floor(canvas_width_pct * ui_width / 100), 6
        else:
            if device_type == "desktop":
                ui_width = device_width - math.floor((device_width * 22) / 100)
            elif device_type == "mobile":
                ui_width = device_width - math.floor((device_width * 13) / 100)
            return ui_width, 1


    def render_doc(self, model, doc_img, canvas_width, doc_height, doc_width):
        height = 1296
        width = 864

        annotations_json = {
            "meta": {
                "version": "v0.1",
                "split": "train",
                "image_id": 0,
                "image_size": {
                    "width": doc_width,
                    "height": doc_height
                }
            },
            "words": []
        }

        st_sparrow_labeling(
            fill_color="rgba(0, 151, 255, 0.3)",
            stroke_width=2,
            stroke_color="rgba(0, 50, 255, 0.7)",
            background_image=doc_img,
            initial_rects=annotations_json,
            height=height,
            width=width,
            drawing_mode="transform",
            display_toolbar=False,
            update_streamlit=False,
            canvas_width=canvas_width,
            doc_height=doc_height,
            doc_width=doc_width,
            image_rescale=True,
            key="doc_annotation" + model.get_image_file()
        )

    def render_results(self, model):
        json_file = model.get_json_file()
        if json_file is not None:
            with open(json_file) as f:
                data_json = json.load(f)
                st.subheader(model.subheader_3)
                st.markdown("---")
                st.json(data_json)
                st.markdown("---")