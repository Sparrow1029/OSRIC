import React from 'react';
import Logo from '../Icons/Logo.js';

const TopBar = () => {
  return (
    <div
    style={{
      backgroundColor: 'black',
      overflow: 'hidden',
      width: '100%',
      height: '8.5vh',
    }}
    >
      <Logo width="100px" height="auto" style={{ position: 'relative', left: '20px', top: '5px' }}/>
    </div>
  )
}

export default TopBar;
