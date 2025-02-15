import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import axios from 'axios';

class ConfirmationScreen extends Component {

  state = {
    btnText: "Confirm"
  }

  handleClick = async () => {
    this.setState({ btnText: "Submitting" });

    console.log("User ID received in ConfirmationScreen:", this.props.userId); // Debugging log

    if (!this.props.userId) {
      console.error("Error: userId is undefined in ConfirmationScreen!");
      return;
    }

    axios.get(`http://localhost:8000/getdatasession?userid=${this.props.userId}`, {
      headers: { Accept: 'application/json' }
    })
    .then(() => {
      this.setState({ btnText: "Done" });
      window.location = "/";
    })
    .catch(() => {
      this.setState({ btnText: "Done" });
      window.location = "/";
    });
  }

  render() {
    return (
      <div style={{ minHeight: '400px' }}>
        <h2>Your consent has been submitted successfully.</h2>
        <p>Click confirm to submit the loan application.</p>
        <strong>Thank You!!!</strong>
        <br /><br />
        <RaisedButton label={this.state.btnText} onClick={this.handleClick} primary />
        <p>After submitting, please wait. This step may take 10-20 seconds.</p>
        <p>Post submission, your application will be under review by the bank admin.</p>
      </div>
    );
  }
}

export default ConfirmationScreen;
