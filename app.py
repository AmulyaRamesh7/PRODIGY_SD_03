import streamlit as st
import pandas as pd
import os

FILE_NAME = "contacts.csv"

# Create file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Name", "Phone", "Email"])
    df.to_csv(FILE_NAME, index=False)

# Load contacts
def load_contacts():
    return pd.read_csv(FILE_NAME)

# Save contacts
def save_contacts(df):
    df.to_csv(FILE_NAME, index=False)

st.title("📞 Simple Contact Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Contact", "View Contacts", "Edit Contact", "Delete Contact"]
)

# ADD CONTACT
if menu == "Add Contact":
    st.subheader("Add New Contact")

    name = st.text_input("Enter Name")
    phone = st.text_input("Enter Phone Number")
    email = st.text_input("Enter Email Address")

    if st.button("Add Contact"):
        if name and phone and email:
            df = load_contacts()
            new_contact = pd.DataFrame([[name, phone, email]],
                                       columns=["Name", "Phone", "Email"])
            df = pd.concat([df, new_contact], ignore_index=True)
            save_contacts(df)
            st.success("Contact Added Successfully!")
        else:
            st.warning("Please fill all fields")

# VIEW CONTACTS
elif menu == "View Contacts":
    st.subheader("Contact List")
    df = load_contacts()
    if df.empty:
        st.info("No contacts available.")
    else:
        st.dataframe(df)

# EDIT CONTACT
elif menu == "Edit Contact":
    st.subheader("Edit Contact")
    df = load_contacts()

    if df.empty:
        st.info("No contacts to edit.")
    else:
        contact_list = df["Name"].tolist()
        selected_contact = st.selectbox("Select Contact", contact_list)

        contact_data = df[df["Name"] == selected_contact].iloc[0]

        new_name = st.text_input("Name", contact_data["Name"])
        new_phone = st.text_input("Phone", contact_data["Phone"])
        new_email = st.text_input("Email", contact_data["Email"])

        if st.button("Update Contact"):
            df.loc[df["Name"] == selected_contact,
                   ["Name", "Phone", "Email"]] = [new_name, new_phone, new_email]
            save_contacts(df)
            st.success("Contact Updated Successfully!")

# DELETE CONTACT
elif menu == "Delete Contact":
    st.subheader("Delete Contact")
    df = load_contacts()

    if df.empty:
        st.info("No contacts to delete.")
    else:
        contact_list = df["Name"].tolist()
        selected_contact = st.selectbox("Select Contact to Delete", contact_list)

        if st.button("Delete Contact"):
            df = df[df["Name"] != selected_contact]
            save_contacts(df)
            st.success("Contact Deleted Successfully!")
