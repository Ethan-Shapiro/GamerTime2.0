import React, { useState, useEffect } from "react";
import { Paper, Box, Button, Typography } from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
import "./ComputerButton.css";
import Overlay from "./Overlay";
import axios from "axios";

const ComputerButton = ({ ID, initData, setCompStatusChange }) => {
  const [backgroundColor, setBackgroundColor] = useState("grey");
  const [open, setOpen] = useState(false);
  const [overlayResponse, setOverlayResponse] = useState(false);
  const [status, setStatus] = useState(0);
  const [timestampMS, setTimestampMS] = useState("");
  const [overlayBtn1, setOverlayBtn1] = useState("");
  const [initialized, setInitialized] = useState(false);
  const [counter, setCounter] = useState("0h 0m 0s");
  const [hoursElapsed, setHoursElapsed] = useState(0);

  const updateCounter = (timestamp = null) => {
    if (timestampMS === "" && timestamp === null) return;
    const now = Date.now();

    // Find the distance between now and the count down date
    const timeElapsed = now - timestampMS;

    // Time calculations for days, hours, minutes and seconds
    var hours = Math.floor(
      (timeElapsed % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((timeElapsed % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeElapsed % (1000 * 60)) / 1000);

    if (hoursElapsed !== hours) {
      setHoursElapsed(hours);
    }

    // Display the result in the element with id="overlayTimer"
    const timeString = hours + "h " + minutes + "m " + seconds + "s";
    setCounter(timeString);
  };

  // Updates the color of the computer button as the person is there for longer
  useEffect(() => {
    if (hoursElapsed >= 5) {
      setBackgroundColor("red");
    } else if (hoursElapsed >= 4) {
      setBackgroundColor("orange");
    } else if (hoursElapsed >= 2) {
      setBackgroundColor("yellow");
    }
  }, [hoursElapsed]);

  useEffect(() => {
    if (timestampMS === "") return;
    setTimeout(updateCounter, 1000);
  }, [counter]);

  useEffect(() => {
    if (initData === null || initialized) return;
    setInitialized(true);
    handleInUseData(initData);
  });

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
    updateCounter(startTimestampMS);
  };

  useEffect(() => {
    if (status === 0) {
      // open the not in use overlay
      setBackgroundColor("grey");
    } else if (status === -1) {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (status > 0) {
      // open end use overlay
      setBackgroundColor("green");
    }
    setCompStatusChange(true);
  }, [status]);

  const handleStop = () => {
    setTimestampMS("");
    setStatus(0);
    setTimeout(() => {
      setCounter("0h 0m 0s");
    }, 500);
  };

  const setInUse = () => {
    axios
      .post(
        "/api/openrec/",
        { computer_id: ID },
        {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("jwt"),
          },
        }
      )
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
      .delete(`/api/openrec/${ID}/${status}`, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
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

  useEffect(() => {
    if (!overlayResponse) return;

    if (status === 0) {
      // open the not in use overlay
      setInUse();
    } else if (status === -1) {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (status > 0) {
      // open end use overlay
      console.log("stopping");
      stopUse();
    }
    setOpen(false);
    setOverlayResponse(false);
  }, [overlayResponse]);

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
        counter={counter}
      ></Overlay>
      <Button sx={{ position: "relative" }} onClick={openOverlay}>
        <div
          style={{
            position: "absolute",
            color: "black",
            fontSize: "1.1vw",
            textTransform: "lowercase",
            top: "-5%",
            left: "25%",
            transform: "translateX(-30%)",
          }}
        >
          {counter}
        </div>
        <div
          style={{
            position: "absolute",
            color: "black",
            textTransform: "lowercase",
            fontSize: "1.1vw",
            top: "-5%",
            left: "90%",
            transform: "translateX(-30%)",
          }}
        >
          {ID}
        </div>
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
