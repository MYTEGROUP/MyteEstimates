from tools.JsonOperators import get_base_path_audio,get_base_path,load_json_data,save_json_data
from UserInterface.ABaPhaseUi import The_Onboarder

def initialize_ui_based_on_status(User_Id,Client_ID,Proposal_ID):
    """Initialize UI based on onboarding and setup completion status."""
    file_name = 'ProposalStatus.json'
    Proposal_Status = load_json_data(file_name)

    if not Proposal_Status:
        # If the status file doesn't exist, initialize it with default values
        proposal_status = {
            "User_Id": f"{User_Id}",
            "Proposal_ID": f"{Proposal_ID}",
            "Client_ID": f"{Client_ID}",
            "proposal_status": "started",
            "ba_phase": False,
            "vision_phase": False,
            "business_verticle_phase": False,
            "Stakeholder_phase": False,
            "Epics_Phase": False,
            "Stories_Phase": False,
            "Tasks_Phase": False,
            "Estimate_Phase": False,
            "ProposalPdf_phase": False,
            "ExcelPhase": False,
            "Email_Sent_Phase": False
        }
        # Save the default values to the file
        save_json_data(file_name, proposal_status)
        # Start the onboarding process
        The_Onboarder()
    else:
        # Load the existing status and proceed accordingly
        print("Loaded existing proposal status:", Proposal_Status)


if __name__ == '__main__':
    User_Id = "001"
    Client_ID = "001"
    Proposal_ID = "001"
    initialize_ui_based_on_status(User_Id, Client_ID, Proposal_ID)