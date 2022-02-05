import React, { useState } from "react";
import "./style.css";

export default function Cell({ cell }) {
  return (
    <div id={cell.id} className="cell">
      {!!cell.value ? cell.value : ""}
    </div>
  );
}
