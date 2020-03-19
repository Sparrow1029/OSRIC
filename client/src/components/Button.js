import React from 'react';
import './Button.css';

const COLORS = [
  "primary",
  "secondary",
  "danger",
]

const VARIANTS = [
  "filled",
  "outline",
]

const SIZES = [
  "medium", 
  "small",
  "large",
]

const Button = ({ children, color, variant, size, onClick, type, disabled }) => {
  const setColor = COLORS.includes(color) ? color : COLORS[0]
  const setVariant = VARIANTS.includes(variant) ? variant : VARIANTS[0]
  const setSize = SIZES.includes(size) ? size : SIZES[0]
  const isDisabled = (disabled !== undefined) ? 'disabled' : false; 
  console.log(color, variant, size, type, onClick, disabled, isDisabled)

  return (
    <button
      className={`btn btn-${setVariant} btn-${setColor} btn-${setSize} ${isDisabled}`}
      onClick={onClick}
      type={type}
      disabled={isDisabled}
    >
      {children}
    </button>
  )
};

export default Button;
