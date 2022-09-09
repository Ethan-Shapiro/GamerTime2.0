import "./App.css";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerLayout from "./components/ComputerLayout";
import ComputerButton from "./components/ComputerButton";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <body className="App-body">
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
          <ComputerButton></ComputerButton>
        </body>
      </ThemeProvider>
    </div>
  );
}

export default App;
