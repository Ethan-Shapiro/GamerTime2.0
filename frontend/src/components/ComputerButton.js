import React, { useState, useEffect } from "react";
import { Paper, Box, Button } from "@mui/material";
import "./ComputerButton.css";
import Overlay from "./Overlay";
import axios from "axios";

const ComputerButton = ({ ID, data }) => {
  const openOverlay = () => {
    setOpen(true);
    if (status === 0) {
      // open the not in use overlay
      setOverlayBtn1("Start");
    } else if (backgroundColor === "red") {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (status > 0) {
      // open end use overlay
      setOverlayBtn1("End");
    }
  };

  const handleInUseData = (data) => {
    const startTimestamp = data["start_timestamp"];
    const startTimestampMS = parseInt(startTimestamp) * 1000;
    setTimestampMS(startTimestampMS);
    setStatus(data["status"]);
    setBackgroundColor("green");
  };

  const handleStop = () => {
    setTimestampMS("");
    setStatus(0);
    setBackgroundColor("grey");
  };

  const [backgroundColor, setBackgroundColor] = useState("grey");
  const [open, setOpen] = useState(false);
  const [overlayResponse, setOverlayResponse] = useState(false);
  const [status, setStatus] = useState(0);
  const [timestampMS, setTimestampMS] = useState("");
  const [overlayBtn1, setOverlayBtn1] = useState("");

  useEffect(() => {
    const setInUse = () => {
      axios
        .post("http://localhost:5050/openrec/", { computer_id: 1 })
        .then((response) => {
          const data = response.data;
          if (data["success"]) {
            handleInUseData(data);
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
        .delete(`http://localhost:5050/openrec/${ID}/${status}`)
        .then((response) => {
          const data = response.data;
          console.log(data);
          if (data["success"]) {
            handleStop();
          } else if (data["status"] > 0) {
            handleInUseData(data);
          }
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
          }
        });
    };

    if (!overlayResponse) return;
    if (status === 0) {
      // open the not in use overlay
      setInUse();
    } else if (status === -1) {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (status > 0) {
      // open end use overlay
      stopUse();
    }
    setOpen(false);
    setOverlayResponse(false);
  }, [ID, overlayResponse, status]);

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
        startTimestampMS={timestampMS}
        btn1Text={overlayBtn1}
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
