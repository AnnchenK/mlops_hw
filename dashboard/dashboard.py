import streamlit as st
import requests
import os


_host = os.environ.get("ADDRESS", "0.0.0.0")
_port = int(os.environ.get("PORT", 0))
_address = f"http://{_host}:{_port}"


def _get_model_list():
    """
    Fetch the list of added models from the service.
    """
    response = requests.get(f"{_address}/list_added")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch model list.")
        return {}


def _retrain_model(model_id):
    """
    Send a request to retrain the specified model.
    """
    response = requests.get(f"{_address}/retrain_model?id={model_id}")
    if response.status_code == 200:
        return f"Model {model_id} retrained successfully."
    else:
        return f"Failed to retrain model {model_id}."


def _remove_model(model_id):
    """
    Send a request to remove the specified model.
    """
    response = requests.get(f"{_address}/remove_model?id={model_id}")
    if response.status_code == 200:
        return f"Model {model_id} removed successfully."
    else:
        return f"Failed to remove model {model_id}."


def main():
    st.title("ML Model Management Dashboard")

    if 'models' not in st.session_state:
        st.session_state.models = _get_model_list()
    if 'message' not in st.session_state:
        st.session_state.message = ""

    models = st.session_state.models

    if models:
        for model_id, model_name in list(models.items()):
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(f"**Model Name:** {model_name} | **ID:** {model_id}")
            with col2:
                if st.button("Retrain", key=f"retrain-{model_id}"):
                    st.session_state.message = _retrain_model(model_id)
                    st.session_state.models = _get_model_list()
            with col3:
                if st.button("Remove", key=f"remove-{model_id}"):
                    st.session_state.message = _remove_model(model_id)
                    del st.session_state.models[model_id]
                    st.rerun()
    else:
        st.info("No models to display. Please add some models.")

    status_container = st.container()
    with status_container:
        if  st.session_state.message:
            st.info(st.session_state.message)


if __name__ == "__main__":
    main()
