import "./App.css";
import { useState, useCallback } from "react";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerLayout from "./components/ComputerLayout";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Queue from "./components/Queue";
import Navbar from "./components/Navbar";
import { Button } from "@mui/material";
import MessageManager from "./components/MessageManager";
import MessageCenter from "./components/MessageCenter";
import axios from "axios";

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

function App() {
  const [compStatusChange, setCompStatusChange] = useState(true);
  const handleCompStatusChange = useCallback((data) => {
    setCompStatusChange(data);
  }, []);

  const { addMessage, messages, removeMessage } = MessageManager();

  async function getAccessToken() {
    return new Promise(function (resolve, reject) {
      let refresh_token = localStorage.getItem("jwt_refresh");
      if (refresh_token === null) {
        console.log(refresh_token);
        return null;
      }
      refresh_token = "Bearer " + refresh_token;

      // use the refresh token to get a new access token
      axios
        .post(
          "/api/auth/refresh",
          {},
          {
            headers: {
              Authorization: refresh_token,
            },
          }
        )
        .then((response) => {
          console.log(response);
          if (response.data["success"]) {
            const accessToken = response.data["access_token"];
            localStorage.setItem("jwt", accessToken);
            resolve("Bearer " + accessToken);
          }
        })
        .catch((error) => {
          localStorage.removeItem("jwt");
          localStorage.removeItem("jwt_refresh");
          console.log(error.response);
          reject("JWT Access and Refresh token expired.");
        });
    }).then((result) => {
      return result;
    });
  }

  const endAllSessions = () => {
    getAccessToken().then((accessToken) => {
      axios
        .post(
          "/api/models/end_all_sessions",
          {},
          {
            headers: {
              Authorization: accessToken,
            },
          }
        )
        .then((response) => {
          console.log(response);
          if (response.data["success"]) {
            window.location.reload(false);
          }
        })
        .catch((error) => {
          console.log(error.response);
          addMessage("Failed to end all computer sessions.", "error");
        });
    });
  };

  return (
    <div className="App">
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <body className="App-body">
          <MessageCenter
            messages={messages}
            removeMessage={removeMessage}
          ></MessageCenter>
          <Navbar
            navbarLabel="Home"
            addMessage={addMessage}
            getAccessToken={getAccessToken}
          ></Navbar>
          <Grid container columnSpacing={1}>
            <Grid container xs={12} sm={9}>
              <Grid container xs={12}>
                <ComputerLayout
                  setCompStatusChange={handleCompStatusChange}
                  addMessage={addMessage}
                  getAccessToken={getAccessToken}
                ></ComputerLayout>
              </Grid>
              <Button
                variant="contained"
                color="error"
                onClick={() => {
                  endAllSessions();
                }}
              >
                END ALL SESSIONS
              </Button>
            </Grid>
            <Grid xs={12} sm={3}>
              <Queue
                setCompStatusChange={handleCompStatusChange}
                compStatusChange={compStatusChange}
                addMessage={addMessage}
                getAccessToken={getAccessToken}
              ></Queue>
            </Grid>
          </Grid>
        </body>
      </ThemeProvider>
    </div>
  );
}

export default App;
