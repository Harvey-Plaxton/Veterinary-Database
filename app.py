# Import the required packages
from datetime import date
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file

#%% Create the Patient Class
class Patient:
    def __init__(self, patient_id, patient_name, owner_name, condition, date_arrival):
        #Setting the variables
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.owner_name = owner_name
        self.condition = condition
        self.date_arrival = date_arrival
#Produce the layout for printing a Patient record.
    def __str__(self):
        return(f"Patient ID: {self.patient_id}, Name: {self.patient_name}, Owner: {self.owner_name}\n"
               f"Condition: {self.condition}, Arrival Date: {self.date_arrival}")
#%%

# Create the Database Class
class Database:
    def __init__(self):
        # Initialize the database as a pandas DataFrame
        self.patients = pd.DataFrame(columns=["Patient ID", "Patient Name", "Owner Name", "Condition", "Date Arrival"])

    def add_patient(self, patient):
        # Append a new patient as a dictionary
        new_patient = {
            "Patient ID": patient.patient_id,
            "Patient Name": patient.patient_name,
            "Owner Name": patient.owner_name,
            "Condition": patient.condition,
            "Date Arrival": patient.date_arrival
        }
        self.patients = pd.concat([self.patients, pd.DataFrame([new_patient])], ignore_index=True)
        
    def visualize_conditions(self):
        """Visualize the distribution of conditions using Bokeh."""
        if self.patients.empty:
            print("No patients in the database to visualize.")
            return

        # Count the occurrences of each condition
        condition_counts = self.patients["Condition"].value_counts()

        # Create a Bokeh bar chart
        p = figure(
            title="Distribution of Patient Conditions",
            x_range=condition_counts.index.tolist(),
            x_axis_label="Condition",
            y_axis_label="Count",
            height=350,
            width=500
            )
        p.vbar(x=condition_counts.index, top=condition_counts.values, width=0.5, color="navy")

        # Specify an output file and show the plot
        output_file("conditions_distribution.html")  # Output will be saved to this file
        show(p)
        
    #Define functions for record searching

    def find_patient_by_id(self, patient_id):
        #Search for matching ID and return the list
        result = self.patients[self.patients["Patient ID"] == patient_id]
        return result if not result.empty else None

    def find_patient_by_name(self, patient_name):
        #Search for matching patient name and return the list
        result = self.patients[self.patients["Patient Name"].str.contains(patient_name, case=False, na=False)]
        return result if not result.empty else None

    def find_patient_by_owner(self, owner_name):
        #Search for matching owner anme and return the list
        result = self.patients[self.patients["Owner Name"].str.contains(owner_name, case=False, na=False)]
        return result if not result.empty else None

    # Define function for deleting a record
    def delete_patient(self, patient_id):
        #Exclude the matching record from the patients list
        self.patients = self.patients[self.patients["Patient ID"] != patient_id]

    #Define the function for modifying a record
    def edit_patient(self, patient_id):
        #Find the record with matching ID
        patient = self.find_patient_by_id(patient_id)
        #Produce user feedback for the record
        if patient is not None:
            print(f"Found patient:\n{patient}")
            #Request confirmation
            confirmation = input("Is this the correct patient? (yes/no): ").lower()
            # Display fields that can be modified
            if confirmation == 'yes':
                new_owner_name = input("Enter new owner's name: ")
                new_patient_name = input("Enter new patient name: ")
                print("New Condition: 1 Mild - 2 Moderate - 3 Severe")
                condition_choice = input("Select a new condition (1-3): ")
                if condition_choice == '1':
                    condition = 'Mild'
                elif condition_choice == '2':
                    condition = 'Moderate'
                elif condition_choice == '3':
                    condition = 'Severe'
                #Provide user feedback on incorrect inputs
                else:
                    print("Invalid choice, no changes made to condition.")
                    return
                #Modify the record with new inputs
                self.patients.loc[self.patients["Patient ID"] == patient_id, ["Owner Name", "Patient Name", "Condition"]] = [
                    new_owner_name, new_patient_name, condition]
                #User feedback for successful update
                print("Patient details updated successfully.")
            else:
                #User feedback for unsuccessful update
                print("Edit operation cancelled.")
        else:
            print("Patient not found.")

    #Define function for returning the database
    def list_patients(self):
        if not self.patients.empty:
            print(self.patients.to_string(index=False))
        else:
            #Provide feedback for an empty database
            print("No patients in the database.")
            
    #Define function to export as csv file. Apply a default if no filename is entered.
    def export_to_csv(self, filename="patients.csv"):
        """Export the list of patients to a CSV file."""
        #Cancel operation for an empty database
        if self.patients.empty:
            print("No patients in the database to export.")
            return
    
        # Ensure the file has a .csv extension
        if not filename.endswith(".csv"):
            filename += ".csv"
            
        #Export and provide user feedback
        self.patients.to_csv(filename, index=False)
        print(f"Patient data exported successfully to {filename}.")
#%%

# Function to display the menu
def display_menu():
    print("\n")
    print("\n Patient Database System \n")
    print("1. Add a new Patient")
    print("2. Search for a patient")
    print("3. List all patients")
    print("4. Delete a Patient")
    print("5. Edit a Patient")
    print("6. Visualize Conditions")
    print("7. Export Patient List to CSV")
    print("8. Exit \n")
    choice = input("Enter your choice (1-8): ")
    return choice
#%%

# Add a new patient
def add_new_patient(database):
    # Provide indexing for the new record
    if not database.patients.empty:
        patient_id = str(int(database.patients["Patient ID"].max()) + 1)
    else:
        patient_id = "1"

    #Display user inputs for required fields
    owner_name = input("Enter owner's name: ")
    patient_name = input("Enter the patient's name: ")
    print("Patient Condition: 1 Mild - 2 Moderate - 3 Severe")
    condition_choice = input("Select a condition (1-3): ")
    if condition_choice == '1':
        condition = 'Mild'
    elif condition_choice == '2':
        condition = 'Moderate'
    elif condition_choice == '3':
        condition = 'Severe'
    else:
        print("Invalid choice, please select option 1, 2, or 3.")
        return

    #Retrieve the date using the datetime library
    today = date.today()
    date_arrival = today.strftime('%B %d, %Y')
    # Create and add the record using the obtained inputs
    new_patient = Patient(patient_id, patient_name, owner_name, condition, date_arrival)
    database.add_patient(new_patient)
    print(f"Patient {patient_id}-{owner_name} added successfully!")
#%%

# Search for a patient
def search_patient(database):
    #Produce options for the various searchign methods and return the relevant choice
    print("Type 1 to search by patient ID. Type 2 to search by Owner name. Type 3 to search by patient name")
    search_choice = input("Enter choice (1-3): ")
    if search_choice == '1':
        patient_id = input("Enter the patient ID to search: ")
        patient = database.find_patient_by_id(patient_id)
        if patient is not None:
            print(patient)
        else:
            print("Patient not found.")
    elif search_choice == '2':
        owner_name = input("Enter the Owner name to search: ")
        patients = database.find_patient_by_owner(owner_name)
        if patients is not None:
            print(f"Found {len(patients)} patient(s) for owner '{owner_name}':")
            print(patients)
        else:
            print("Patient not found. Beware of case sensitivity when searching.")
    elif search_choice == '3':
        patient_name = input("Enter the patient's name: ")
        patients = database.find_patient_by_name(patient_name)
        if patients is not None:
            print(f"Found {len(patients)} patient(s) under the name '{patient_name}':")
            print(patients)
        else:
            print("Patient not found. Beware of case sensitivity when searching.")
    #Provide feedback for an incorrect selection
    else:
        print("Invalid Choice, please choose option 1, 2, or 3.")
#%%

# Delete a patient
def remove_patient(database):
    #Request a patient ID
    patient_id = input("Enter patient ID: ")
    patient = database.find_patient_by_id(patient_id)
    if patient is not None:
        print(patient)
        print(f"Delete patient {patient_id}")
        #Request confirmation for deletion
        confirmation = input("Type 1 to confirm: ")
        if confirmation == '1':
            database.delete_patient(patient_id)
            print(f"Patient {patient_id} has been successfully deleted")
        else:
            print("Operation cancelled")
    #Provide feeback when a matching record is not obtained
    else:
        print("Patient not found.")
#%%

# Main program
if __name__ == "__main__":
    db = Database()

    while True:
        # Produce the interactive menu
        choice = display_menu()

        # Run functions associated with user input
        if choice == '1':
            add_new_patient(db)
        elif choice == '2':
            search_patient(db)
        elif choice == '3':
            db.list_patients()
        elif choice == '4':
            remove_patient(db)
        elif choice == '5':
            patient_id = input("Enter the patient ID to edit: ")
            db.edit_patient(patient_id)
        elif choice == '6':
            db.visualize_conditions()
        elif choice == '7':
            #Request an optional filename
            filename = input("Enter the filename to save as (default: patients.csv): ").strip()
            if not filename:
                filename = "patients.csv"
            db.export_to_csv(filename)
        #Option to end the program
        elif choice == '8':
            print("Closing Program")
            break
        else:
            print("Invalid choice. Please select a valid option.")
