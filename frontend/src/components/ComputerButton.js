import React, { useState, useEffect, useRef } from "react";
import { Paper, Box, Button, Typography, Tooltip } from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
import "./ComputerButton.css";
import Overlay from "./Overlay";
import axios from "axios";

const ComputerButton = ({
  Name,
  ID,
  initData,
  setCompStatusChange,
  addMessage,
  getAccessToken,
}) => {
  const [backgroundColor, setBackgroundColor] = useState("grey");
  const [open, setOpen] = useState(false);
  const [overlayResponse, setOverlayResponse] = useState(false);
  const [status, setStatus] = useState(0);
  const [startTimestampMS, setStartTimestampMS] = useState(0);
  const [overlayBtn1, setOverlayBtn1] = useState("");
  const [counter, setCounter] = useState("00:00:00");
  const initialized = useRef(false);
  const intervalID = useRef(undefined);

  // tooltip states
  const [popupText, setPopupText] = useState("");
  const [popupOpen, setPopupOpen] = useState(false);

  useEffect(() => {
    if (initData === null || initialized.current) return;

    // set initialized to true so we don't reinitialize
    initialized.current = true;

    // handle conflict popup
    if ("conflict" in initData) handleTimeConflict(initData);

    // update the button's attributes using the initial data
    if ("id" in initData) handleInUseData(initData);
  }, [initData]);

  // When the startTimestamp changes
  // either setTimeout for color changes
  // or do nothing
  useEffect(() => {
    if (startTimestampMS === 0) return;

    const updateTimer = () => {
      console.log("in update timer");
      // calculate the various time until color changes
      const now = Date.now();

      // Find the distance between now and the count down date
      const timeElapsed = now - startTimestampMS;

      // Time calculations for hours, minutes and seconds
      const hours = Math.floor(
        (timeElapsed % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const minutes = Math.floor(
        (timeElapsed % (1000 * 60 * 60)) / (1000 * 60)
      );
      var seconds = Math.floor((timeElapsed % (1000 * 60)) / 1000);

      // TEST
      let totalMinutes = hours * 60 + minutes;
      // totalMinutes = minutes * 60 + seconds;

      // create different timeouts if necessary
      // yellow, orange, and red are at 60, 90, and 120 minutes from start
      if (totalMinutes >= 120) {
        // create no timeouts if we are here because color will next change.
        setBackgroundColor("red");
      } else if (totalMinutes >= 90) {
        // create timeout for red color change
        setBackgroundColor("orange");
      } else if (totalMinutes >= 60) {
        // create timeout for orange and red color change
        setBackgroundColor("yellow");
      } else {
        setBackgroundColor("green");
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

    // update every second
    const newIntervalID = setInterval(() => updateTimer(), 1000);
    intervalID.current = newIntervalID;

    return () => {
      clearInterval(intervalID.current);
    };
  }, [startTimestampMS]);

  const handleTimeConflict = (initData) => {
    // split into start and end time
    const start_end_time = initData["conflict"].split("-");

    // get conflict start and end hour/minutes
    const start_hour = start_end_time[0].split(":")[0];
    const start_minutes = start_end_time[0].split(":")[1];

    const end_hour = start_end_time[1].split(":")[0];
    const end_minutes = start_end_time[1].split(":")[1];

    // get start offset from current time
    let currDate = new Date();
    let hourOffset = currDate.getHours() - start_hour;
    let minuteOffset = currDate.getMinutes() - start_minutes;

    // set timer to open popup 30 minutes before esports
    currDate.setHours(currDate.getHours() + 2);
    console.log(currDate);

    // set timer to update text at 15, 10, and 5 minutes

    // set timer to disable computer button until end of esports
  };

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

  const handleInUseData = (data) => {
    // set current status
    // if disabled, no timestamp exists so return
    setStatus(data["status"]);
    if (data["status"] === -1) return;

    // convert start timestamp to an int, convert to milliseconds, and
    // save start timestamp to the attribute
    const startTimestamp = data["start_timestamp"];
    const startTimestampMS = parseInt(startTimestamp) * 1000;
    setStartTimestampMS(startTimestampMS);

    // Check if there are any esports overlapping blocks
    if (data["esports"]) {
      // find the time offset from now until the esports
      // tooltip should be opened
      // add 30 minutes for time tooltip should be closed
      // open esports tooltip using offset
      // close esports tooltip using offset
    }
  };

  const handleStop = () => {
    setStartTimestampMS(0);
    setStatus(0);
    setCounter("00:00:00");
    clearInterval(intervalID.current);
    intervalID.current = undefined;
  };

  function setInUse() {
    getAccessToken()
      .then((accessToken) => {
        axios
          .post(
            "/api/openrec/",
            { computer_id: ID },
            {
              headers: {
                Authorization: accessToken,
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
              addMessage("Unauthorized Request! Please login!", "error");
            }
          });
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function stopUse() {
    getAccessToken()
      .then((accessToken) => {
        console.log("got access token");
        console.log(accessToken);
        axios
          .delete(`/api/openrec/${ID}/${status}`, {
            headers: {
              Authorization: accessToken,
            },
          })
          .then((response) => {
            const data = response.data;
            console.log(data);
            if (data["status"] > 0) {
              addMessage(`Different computer ${ID} session started!`, "info");
              handleInUseData(data);
            } else {
              handleStop();
            }
          })
          .catch((error) => {
            if (error.response) {
              addMessage("Unauthorized Request! Please login!", "error");
              console.log(error.response);
            }
          });
      })
      .catch((error) => {
        console.log(error);
      });
  }

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
        startTimestampMS={startTimestampMS}
        btn1Text={overlayBtn1}
        counter={counter}
      ></Overlay>
      <Tooltip
        title="Esports in 30 minutes"
        open={true}
        placement={"top"}
        arrow
      >
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
              textTransform: "uppercase",
              fontSize: "1.1vw",
              top: "-5%",
              left: "87%",
              transform: "translateX(-30%)",
            }}
          >
            {Name}
          </div>
          <Box
            component="img"
            sx={{ height: "80%", width: "80%" }}
            alt="Gamer Time Image"
            src="GamerTimelogo.png"
          ></Box>
        </Button>
      </Tooltip>
    </Paper>
  );
};

export default ComputerButton;
