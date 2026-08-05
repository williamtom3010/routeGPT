import streamlit as st
import test


# Streamlit UI
def main():
    st.title("RouteGPT")
    
    # User input prompt
    # displays the title in UI
    prmpt = st.text_area("Enter your prompt:", "")
    
    # Override switch
    # provides a radio switch to select yes or no
    over_ride = st.radio("Do you want to manually select the model?", ["No", "Yes"], index=0)


    # response = test.main_app(prmpt, over_ride)
    # calls the function main_app from test.py
    response = test.main_app(prmpt, over_ride)
    # button provided in the ui
    if st.button("Generate Output"):
                        
        st.subheader("Generated Output:")
        st.write(response)
        
        # Save to PostgreSQL
        test.save_to_database(prmpt, response)
        st.success("Data saved to PostgreSQL database!")
        # Save to NoSQL
        test.save_to_no_sql_database(prmpt, response)
        st.success("Data saved to NoSQL database!")


if __name__ == "__main__":
    main()