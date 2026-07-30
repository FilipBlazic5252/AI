import { useState } from "react";
import Canvas from "./Canvas";

function App() {
  const [digit, setDigit] = useState(null);
  const [confidence, setConfidence] = useState(null);
  return (
    <div className="container">
      <h1>AI Digit Recognizer</h1>
      <Canvas
        setDigit={setDigit}
        setConfidence={setConfidence}
      />
      <div className="result">
        <h2>
          Prediction
        </h2>
        <h1>
          {digit ?? "-"}
        </h1>
        <p>
          Confidence
          <br />
          {confidence ?? "-"}
        </p>
      </div>
    </div>
  );
}

export default App;