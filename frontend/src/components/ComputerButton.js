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
  const [timestampMS, setTimestampMS] = useState(0);
  const [overlayBtn1, setOverlayBtn1] = useState("");
  const [initialized, setInitialized] = useState(false);
  const [counter, setCounter] = useState("00:00:00");
  const [hoursElapsed, setHoursElapsed] = useState(0);
  const [intervalTimer, setIntervalTimer] = useState(undefined);

  useEffect(() => {
    if (initData === null || initialized) return;
    setInitialized(true);
    handleInUseData(initData);
  }, []);

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

  const openOverlay = () => {
    setOpen(true);
    if (status === 0) {
      // open the not in use overlay
      setOverlayBtn1("Start");
    } else if (status === -1) {
      // open enable pc overlay
      setBackgroundColor("red");
    } else if (status > 0) {
      // open end use overlay
      setOverlayBtn1("End");
    }
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

  useEffect(() => {
    const updateCounter = () => {
      console.log(timestampMS);
      if (timestampMS === 0) return;

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

      let minutesString = "";
      if (minutes < 10) {
        minutesString = "0" + minutes;
      } else {
        minutesString += minutes;
      }

      let secondsString = "";
      if (seconds < 10) {
        secondsString = "0" + seconds;
      } else {
        secondsString += seconds;
      }

      // Display the result in the element with id="overlayTimer"
      const timeString =
        "0" + hours + ":" + minutesString + ":" + secondsString;
      setCounter(timeString);
    };
    updateCounter(timestampMS);
    const interval = setInterval(updateCounter, 1000);
    setIntervalTimer(interval);
  }, [timestampMS, hoursElapsed]);

  const handleInUseData = (data) => {
    const startTimestamp = data["start_timestamp"];
    const startTimestampMS = parseInt(startTimestamp) * 1000;
    setTimestampMS(startTimestampMS);
    setStatus(data["status"]);
  };

  const handleStop = () => {
    setTimestampMS(0);
    setStatus(0);
    setCounter("00:00:00");
    clearInterval(intervalTimer);
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
            left: "20%",
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
