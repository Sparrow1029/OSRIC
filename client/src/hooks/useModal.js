import React, { useState } from 'react';
import Modal from '../components/Modal';

const useModal = () => {
  const [isShowing, setIsShowing] = useState(false);

  const toggle = () => {
    setIsShowing(!isShowing);
  }
  
  const RenderModal = ({ children }: { children: React.ReactChild }) => (
    <React.Fragment>
      {isShowing && <Modal isShowing={isShowing} hide={toggle}>{children}</Modal>}
    </React.Fragment>
  )

  return {
    toggle,
    RenderModal,
  }
};

export default useModal;
