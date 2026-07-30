import { useState } from "react";
import Canvas from "./Canvas";
import RoutedApp from "./RoutedApp";

function App() {

  const [digit, setDigit] = useState(null);
  const [confidence, setConfidence] = useState(null);

  return (
    <RoutedApp />

  );

}

export default App;