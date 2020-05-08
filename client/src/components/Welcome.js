import React, { useState } from 'react';
import Button from './Button.js';
// import Modal from './Modal';
import useModal from '../hooks/useModal';
import './Welcome.css';

import Dragon from '../Icons/Dragon.js';

const Welcome = () => {
  const {toggle: toggleLogin, RenderModal: RenderLogin} = useModal();
  const {toggle: toggleRegister, RenderModal: RenderRegister} = useModal();

  return (
    <div className="container">
      <RenderLogin>
        <div>
          <h1>This is the login form</h1>
          <form>
            <input type="text" placeholder="Username"/>
            <input type="text" placeholder="Password"/>
          </form>
        </div>
      </RenderLogin>
      <RenderRegister>
        <div>
          <h2>Register here</h2>
          <form>
            <input type="text" placeholder="Name" />
            <input type="text" placeholder="Email" />
          </form>
        </div>
      </RenderRegister>
      <div className="welcome-main">
        <div style={{ /*minWidth: 250,*/ display: 'inline' }}>
          <Button
            variant="filled"
            color="secondary"
            size="large"
            type="input" 
            onClick={toggleLogin}
          >
            Login
          </Button>
          <Button
            variant="filled"
            color="primary"
            size="large"
            type="input"
            onClick={toggleRegister}
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
