import "./App.css";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerLayout from "./components/ComputerLayout";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Queue from "./components/Queue";
import Navbar from "./components/Navbar";

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
          <Navbar navbarLabel="Home"></Navbar>
          <Grid container columnSpacing={1}>
            <Grid xs={12} sm={9}>
              <ComputerLayout></ComputerLayout>
            </Grid>
            <Grid xs={12} sm={3}>
              <Queue></Queue>
            </Grid>
          </Grid>
        </body>
      </ThemeProvider>
    </div>
  );
}

export default App;
