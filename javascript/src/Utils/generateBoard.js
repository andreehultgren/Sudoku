export default function generateBoard() {
  // Create an empty board
  let board = Array(81).fill({
    value: 0,
    locked: false,
    incorrect: false,
    id: null,
  });

  board = board.map((data, index) => ({
    ...data,
    id: index,
  }));

  return board;
}
