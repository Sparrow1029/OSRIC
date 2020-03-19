import React from 'react';
import Button from './Button.js';
import './Welcome.css';

import Dragon from '../Icons/Dragon.js';

const Welcome = () => {
  return (
    <div className="container">
      <div className="welcome-main">
        <div style={{ /*minWidth: 250,*/ display: 'inline' }}>
          <Button
            variant="filled"
            color="primary"
            size="large"
            type="input" 
            onClick={() => {console.log("Logging in...")}}
          >
            Login
          </Button>
          <Button
            variant="filled"
            color="secondary"
            size="large"
            type="input"
            onClick={() => {console.log('You\'re registering')}}
          >
            Register
          </Button>
        </div>
        <h1>Welcome to D&amp;D Database!</h1>
        <div style={{ maxWidth: 800, minWidth: 200, alignSelf: 'center' }}>
        <p>
        A database and management tool for Players, Parties, and DMs playing OSRIC (AD&amp;D) 1st edition
        </p>
      </div>
      {/*
        <Dragon width="100%" height="auto" fillOpacity="0.08"/>
      */}
        <div style={{ alignSelf: 'center', maxWidth: 800}}>
          <Dragon width="100%" height="auto"/>
        </div>
      </div>
    </div>
  )
}

export default Welcome;
