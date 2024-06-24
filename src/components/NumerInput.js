"use client";
import { useState } from "react";

function NumberInput({ onInputChange }) {
  const [isRandom, setIsRandom] = useState(true);
  const [inputValue, setInputValue] = useState("");

  const generateRandomNumbers = () => {
    let randomNumbers = "";
    for (let i = 0; i < 10; i++) {
      // Generar 10 números aleatorios
      randomNumbers += Math.floor(Math.random() * 10);
    }
    return randomNumbers;
  };

  const handleRadioChange = (e) => {
    const value = e.target.value === "random";
    setIsRandom(value);
    if (value) {
      const randomNumbers = generateRandomNumbers();
      setInputValue(randomNumbers);
      onInputChange(randomNumbers);
    } else {
      setInputValue("");
      onInputChange("");
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value.replace(/\s+/g, ""); // Remover espacios
    setInputValue(value);
    onInputChange(value);
  };

  return (
    <div className="mb-4 mt-4 ml-4 flex items-center">
      <label className="mr-4 text-white">
        <input
          type="radio"
          name="mode"
          value="random"
          checked={isRandom}
          onChange={handleRadioChange}
          className="text-white"
        />
        Random
      </label>
      <label>
        <input
          type="radio"
          name="mode"
          value="manual"
          checked={!isRandom}
          onChange={handleRadioChange}
          className="text-white"
        />
        Manual
      </label>
      {!isRandom && (
        <input
          type="text"
          placeholder="Enter numbers without spaces"
          value={inputValue}
          onChange={handleInputChange}
           className="ml-2 p-2 border rounded bg-[#2e2e2e] text-white w-64"
        />
      )}
    </div>
  );
}

export default NumberInput;
