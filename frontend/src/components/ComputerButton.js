import React, { useState, useEffect } from "react";
import { Paper, Box, Button } from "@mui/material";
import "./ComputerButton.css";
import Overlay from "./Overlay";
import axios from "axios";

const ComputerButton = ({ ID }) => {
  const openOverlay = () => {
    if (backgroundColor === "grey") {
      // open the not in use overlay
      setOpen(true);
      setBackgroundColor("grey");
    } else if (backgroundColor === "red") {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (backgroundColor === "green") {
      // open end use overlay
      setBackgroundColor("green");
    }
  };
  const [backgroundColor, setBackgroundColor] = useState("grey");
  const [open, setOpen] = useState(false);
  const [overlayResponse, setOverlayResponse] = useState(false);

  const fetchTest = async () => {
    const response = await fetch("http://localhost:5050/openrec", {
      method: "get",
      mode: "cors",
    });
    console.log(response.json());
  };

  const setInUse = () => {
    axios
      .get("http://localhost:5050/openrec", { computer_id: ID })
      .then((response) => {
        const data = response.data.data;
        if (data["success"]) {
          // add items to session
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  };

  const stopUse = () => {
    axios
      .get("http://localhost:5050/openrec", { computer_id: ID })
      .then((response) => {
        const data = response.data.data;
        if (data["success"]) {
          // add items to session
        }
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  };

  useEffect(() => {
    // if the overlay response is false, do nothing
    if (!overlayResponse) {
      return;
    }
    if (backgroundColor === "grey") {
      console.log("We're making our request!");
      setInUse();
    } else if (backgroundColor === "red") {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (backgroundColor === "green") {
      // open end use overlay
      stopUse();
      setBackgroundColor("green");
    }
  }, [overlayResponse, backgroundColor]);

  return (
    <Paper
      elevation={15}
      sx={{
        height: "100%",
        width: "100%",
        backgroundColor: { backgroundColor },
      }}
    >
      <Overlay
        open={open}
        setOpen={setOpen}
        setOverlayResponse={setOverlayResponse}
      ></Overlay>
      <Button onClick={openOverlay}>
        <Box
          component="img"
          sx={{ height: "80%", width: "80%" }}
          alt="Gamer Time Image"
          src="GamerTimelogo.png"
        ></Box>
      </Button>
    </Paper>
  );
};

export default ComputerButton;
