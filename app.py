import json
import os
import streamlit as st

st.set_page_config(page_title="Grand Line Bounty Board", page_icon="🏴‍☠️")

st.title("🏴‍☠️ Grand Line Bounty Board")
st.markdown("Welcome, Bounty Hunter! Access and expand the World Government's most wanted database.")

DATA_FILE = "bounty_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

bounties = load_data()

# Sidebar navigation
option = st.sidebar.selectbox("Navigation", ["View Bounty Board", "Search Target", "Add New Target"])

if option == "View Bounty Board":
    st.subheader("Current Active Bounties")
    if bounties:
        for b in bounties:
            st.info(f"**{b.get('name')}** — *{b.get('epitaph', 'No Epitaph')}* \n\n 💰 **Bounty:** {b.get('bounty')} | **Status:** {b.get('status')}")
    else:
        st.warning("No targets found in the database.")

elif option == "Search Target":
    st.subheader("Search the Database")
    query = st.text_input("Enter character name or keyword:").lower()
    if query:
        results = [b for b in bounties if query in b.get("name", "").lower() or query in b.get("epitaph", "").lower()]
        if results:
            for r in results:
                st.success(f"Found: **{r.get('name')}** ({r.get('bounty')})")
        else:
            st.error("No matching targets found.")

elif option == "Add New Target":
    st.subheader("Register a New Target")
    with st.form("bounty_form"):
        name = st.text_input("Character Name")
        epitaph = st.text_input("Epitaph / Title")
        bounty = st.text_input("Bounty Amount")
        status = st.selectbox("Status", ["Active", "Captured", "Deceased"])
        submitted = st.form_submit_button("Add to Board")
        
        if submitted and name:
            new_target = {"name": name, "epitaph": epitaph, "bounty": bounty, "status": status}
            bounties.append(new_target)
            with open(DATA_FILE, "w") as f:
                json.dump(bounties, f, indent=4)
            st.success(f"Successfully added {name} to the database!")