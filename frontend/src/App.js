import "./App.css";
import { useState } from "react";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerLayout from "./components/ComputerLayout";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Queue from "./components/Queue";
import Navbar from "./components/Navbar";
import MessageManager from "./components/MessageManager";
import MessageCenter from "./components/MessageCenter";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App() {
  const [compStatusChange, setCompStatusChange] = useState(true);

  const { addMessage, messages, removeMessage } = MessageManager();

  return (
    <div className="App">
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <body className="App-body">
          <MessageCenter
            messages={messages}
            removeMessage={removeMessage}
          ></MessageCenter>
          <Navbar navbarLabel="Home" addMessage={addMessage}></Navbar>
          <Grid container columnSpacing={1}>
            <Grid xs={12} sm={9}>
              <ComputerLayout
                compStatusChange={compStatusChange}
                setCompStatusChange={setCompStatusChange}
                addMessage={addMessage}
              ></ComputerLayout>
            </Grid>
            <Grid xs={12} sm={3}>
              <Queue
                setCompStatusChange={setCompStatusChange}
                compStatusChange={compStatusChange}
                addMessage={addMessage}
              ></Queue>
            </Grid>
          </Grid>
        </body>
      </ThemeProvider>
    </div>
  );
}

export default App;
