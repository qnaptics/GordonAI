import streamlit as st
import random
from datetime import datetime, timedelta

# Initialize session state
if 'calendar' not in st.session_state:
    st.session_state.calendar = {}
    
    # Generate calendar for the week (Sunday to Saturday)
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    time_slots = ["09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00"]
    
    for day in days:
        st.session_state.calendar[day] = {slot: "available" for slot in time_slots}
    
    # Block random slots for specific people
    people = ["Emma", "Ella", "Jason", "Maya", "Ashok", "Tina"]
    for day in days:
        for _ in range(random.randint(1, 3)):  # Block 1 to 3 slots per day
            slot = random.choice(time_slots)
            if st.session_state.calendar[day][slot] == "available":
                st.session_state.calendar[day][slot] = random.choice(people)

def get_available_slots():
    return {day: [slot for slot, status in slots.items() if status == "available"] 
            for day, slots in st.session_state.calendar.items()}

def book_slot(day, slot, name):
    if st.session_state.calendar[day][slot] == "available":
        st.session_state.calendar[day][slot] = name
        return True
    return False

st.title("Gordon's Professional Scheduling Assistant")

user_input = st.text_input("How may I assist you with Gordon's schedule?")

if user_input:
    if "availability" in user_input.lower():
        available_slots = get_available_slots()
        response = "Gordon's availability for the upcoming week:\n\n"
        for day, slots in available_slots.items():
            if slots:
                response += f"{day}: {', '.join(slots)}\n"
            else:
                response += f"{day}: Fully booked\n"
        st.text_area("Availability", response, height=300, disabled=True)
    elif "book" in user_input.lower():
        available_slots = get_available_slots()
        days_with_slots = [day for day, slots in available_slots.items() if slots]
        
        if days_with_slots:
            col1, col2 = st.columns(2)
            with col1:
                selected_day = st.selectbox("Select a day:", days_with_slots)
            with col2:
                slot_to_book = st.selectbox("Select a time slot:", available_slots[selected_day])
            
            user_name = st.text_input("Your name:")
            
            if st.button("Confirm Booking"):
                if book_slot(selected_day, slot_to_book, user_name):
                    st.success(f"""
                    Booking Confirmed
                    ----------------
                    Day: {selected_day}
                    Time: {slot_to_book}
                    Name: {user_name}
                    """)
                else:
                    st.error("We apologize, but the selected slot is no longer available. Please choose another time.")
        else:
            st.warning("We regret to inform you that there are no available slots for the entire week.")
    else:
        st.info("I apologize, but I didn't understand your request. You can inquire about availability or book a slot.")

# Debug: Print the entire calendar (comment out or remove in production)
# st.write(st.session_state.calendar)