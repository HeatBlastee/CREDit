import React from "react";
import TextField from "material-ui/TextField";
import RaisedButton from "material-ui/RaisedButton";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import AutoComplete from "material-ui/AutoComplete";
import axios from 'axios';
import { stateData } from "./util/stateData";

export default class Form extends React.Component {
  state = {
    name: "",
    mobileNumber: "",
    typeOfBusiness: "",
    businessAddress: "",
    businessDistrict: "",
    businessPinCode: "",
    businessState: "",
    amountApplied: "",
    applyButtonText: "Apply",
    data: stateData
  };

  inputStyles = { width: "512px" };

  change = (e) => {
    const { name, value } = e.target;
    
    // Convert numeric fields to numbers
    this.setState({ 
      [name]: name === "amountApplied" || name === "businessPinCode" || name === "mobileNumber" 
        ? value.replace(/\D/g, '') // Remove non-numeric characters
        : value
    });
  };
  

  onNewRequest = (chosenRequest) => {
    this.setState({ businessState: chosenRequest.value });
  };

  validate = () => {
    let isError = false;
    const errors = {};

    if (this.state.mobileNumber.length !== 10) {
      isError = true;
      errors.mobileNumberError = "Please enter a valid 10-digit mobile number";
    }

    if (!this.state.typeOfBusiness) {
      isError = true;
      errors.typeOfBusinessError = "Please enter your business type";
    }

    if (!this.state.businessDistrict) {
      isError = true;
      errors.businessDistrictError = "Please enter your district";
    }

    if (this.state.businessPinCode.length !== 6) {
      isError = true;
      errors.businessPinCodeError = "Please enter a valid 6-digit pincode";
    }

    if (!this.state.amountApplied) {
      isError = true;
      errors.amountAppliedError = "Please enter the loan amount";
    }

    if (!this.state.businessState) {
      isError = true;
      errors.businessStateError = "Please enter your state";
    }

    this.setState(errors);
    return isError;
  };

  onSubmit = async (e) => {
    e.preventDefault();
  
    this.setState({ applyButtonText: "Applying....." });
  
    const responseData = {
      name: this.state.name,
      mobileNumber: parseInt(this.state.mobileNumber, 10) || 0, // Ensure number type
      typeOfBusiness: this.state.typeOfBusiness,
      businessAddress: this.state.businessAddress,
      businessDistrict: this.state.businessDistrict,
      businessPinCode: parseInt(this.state.businessPinCode, 10) || 0, // Ensure number type
      businessState: this.state.businessState,
      amountApplied: parseFloat(this.state.amountApplied) || 0, // Convert to number
      applicationStatus: 0
    };
  
    try {
      const response = await axios.post("http://localhost:8000/addborrower", responseData, {
        headers: { "Content-Type": "application/json" }
      });
  
      console.log("Full Response Data:", response);
      console.log("User ID from response:", response.data.userId);
  
      if (response.data && response.data.userId) {
        this.props.onFormSubmit(response.data.userId);
      } else {
        console.error("Error: userId not received in response.");
      }
    } catch (error) {
      console.error("Error submitting form:", error.response ? error.response.data : error);
    }
  };
    
  

  render() {
    return (
      <form>
        <TextField
          name="name"
          hintText="Full name"
          floatingLabelText="Full name"
          value={this.state.name}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <TextField
          name="mobileNumber"
          hintText="Mobile Number"
          floatingLabelText="Mobile Number"
          type="number"
          value={this.state.mobileNumber}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <SelectField
          hintText="Type of Business"
          floatingLabelText="Type of Business"
          value={this.state.typeOfBusiness}
          onChange={(event, index, value) => this.setState({ typeOfBusiness: value })}
          style={this.inputStyles}
        >
          <MenuItem value="fashion" primaryText="Fashion" />
          <MenuItem value="hospitality" primaryText="Hospitality" />
          <MenuItem value="jewellery" primaryText="Diamond, Gems and Jewellery" />
          <MenuItem value="entertainment" primaryText="Entertainment" />
          <MenuItem value="daily-essentials" primaryText="Daily Essentials" />
        </SelectField>
        <br />
        <TextField
          name="businessAddress"
          hintText="Business Address"
          floatingLabelText="Business Address"
          value={this.state.businessAddress}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <TextField
          name="businessDistrict"
          hintText="District"
          floatingLabelText="District"
          value={this.state.businessDistrict}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <TextField
          name="businessPinCode"
          hintText="Pincode"
          floatingLabelText="Pincode"
          value={this.state.businessPinCode}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <AutoComplete
          name="businessState"
          hintText="State"
          floatingLabelText="State"
          value={this.state.businessState}
          onChange={this.change}
          dataSource={this.state.data}
          onNewRequest={this.onNewRequest}
          style={this.inputStyles}
          fullWidth={true}
        />
        <br />
        <TextField
          name="accountNumber"
          hintText="Account Number"
          floatingLabelText="Account Number"
          type="number"
          // value={this.state.amountApplied}
          onChange={this.change}
          style={this.inputStyles}
        /><br/>
        <TextField
          name="PANNumber"
          hintText="PAN Number"
          floatingLabelText="PAN Number"
          type="text"
          // value={this.state.amountApplied}
          onChange={this.change}
          style={this.inputStyles}
        /><br/>
        <TextField
          name="accountEmail"
          hintText="Account Email"
          floatingLabelText="Account Email"
          type="text"
          // value={this.state.amountApplied}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br/>
        <TextField
          name="amountApplied"
          hintText="Amount"
          floatingLabelText="Amount"
          type="number"
          value={this.state.amountApplied}
          onChange={this.change}
          style={this.inputStyles}
        />
        <br />
        <RaisedButton label={this.state.applyButtonText} onClick={this.onSubmit} primary />
      </form>
    );
  }
}
