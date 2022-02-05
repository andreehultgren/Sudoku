import React, { useState, useEffect } from "react";
import { generateBoard } from "./Utils";
import Board from "./Board";
import Cell from "./Cell";

function App() {
  const [board, setBoard] = useState(generateBoard());

  const selectClickedCell = (e) => {
    [...document.getElementsByClassName("selected")].forEach((item) =>
      item.classList.remove("selected")
    );
    e.target.classList.add("selected");
  };

  const addNumber = (e) => {
    if (e.code.includes("Digit")) {
      const number = parseInt(e.key);
      const selectedBoxes = [...document.getElementsByClassName("selected")];
      const ids = selectedBoxes.map((element) => parseInt(element.id));
      let newBoard = [...board];
      ids.forEach((id) => {
        newBoard[id].value = number;
      });
      setBoard(newBoard);
      selectedBoxes.forEach((element) => element.classList.remove("selected"));
    }
  };

  useEffect(() => {
    window.addEventListener("click", selectClickedCell);
    window.addEventListener("keyup", addNumber);
    return () => {
      window.removeEventListener("click", selectClickedCell);
      window.removeEventListener("keyup", addNumber);
    };
  }, []);

  return (
    <Board>
      {board.map((cell) => (
        <Cell key={cell.id} cell={cell} />
      ))}
    </Board>
  );
}

export default App;
