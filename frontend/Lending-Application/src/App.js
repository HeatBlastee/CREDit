import React, { Component } from "react";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import "./App.css";
import Form from "./Form";
import ConfirmationScreen from "./ConfirmationScreen";
import NavBar from "./NavBar";

const CONFIRM_STATE = "ConfirmState";

class App extends Component {
  state = {
    showPage: "",
    userId: null // Ensure userId starts as null
  };

  // Function to handle form submission and navigate to ConfirmationScreen
  onFormSubmit = (userId) => {
    console.log("User ID received:", userId); // Debugging log
    this.setState({ showPage: CONFIRM_STATE, userId });
  };

  render() {
    return (
      <MuiThemeProvider>
        <div className="App">
          <NavBar title={"Apply for Business Loans"} />
          
          {/* Conditionally render the Form or ConfirmationScreen */}
          {this.state.showPage !== CONFIRM_STATE ? (
            <Form onFormSubmit={this.onFormSubmit} />
          ) : (
            <ConfirmationScreen userId={this.state.userId} />
          )}
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
