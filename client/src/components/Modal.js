import React, { useEffect } from "react";
import { createPortal } from "react-dom";
import styled from "styled-components";
import PropTypes from "prop-types";


// const Portal = ({ children }) => {
// 	const modalRoot = document.getElementById("modal");
// 	const el = document.createElement("div");
// 
// 	useEffect(() => {
// 	  modalRoot.appendChild(el);	
// 
//     return () => modalRoot.removeChild(el);
// 	}, []);
// 
//   return createPortal(children, el);
// 
// };


const Modal = ({ children, isShowing, hide }) => isShowing ? createPortal(
  <>
    <ModalWrapper>
      <ModalCard>
        <CloseButton onClick={hide}>
          <img src="https:icon.now.sh/x/ff0000" alt="close" />
        </CloseButton>
          {children}
      </ModalCard>
    </ModalWrapper>
    <Background onClick={hide} />
  </>
  , document.getElementById("modal")
) : null;

export default Modal;

Modal.propTypes = {
  // children: PropTypes.arrayOf(PropTypes.object).isRequired,
  children: PropTypes.object.isRequired,
  hide: PropTypes.func.isRequired,
  isShowing: PropTypes.bool.isRequired
};

const ModalWrapper = styled.div`
  position: fixed;  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
`;

const ModalCard = styled.div`
  position: relative;
  min-width: 320px;
  z-index: 100;
  margin-bottom: 100px;
  background: white;
  border-radius: 5px;
  padding: 15px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
`;

const CloseButton = styled.div`
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  background: transparent;
  padding: 10px;
  &:hover {
    cursor: pointer;
  }`;

const Background = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: black;
  opacity: 0.75;
`;
