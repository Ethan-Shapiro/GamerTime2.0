import React, { useEffect, useState } from "react";
import { Backdrop, Box, Button, Typography } from "@mui/material";

const Overlay = ({
  open,
  setOpen,
  setOverlayResponse,
  startTimestampMS,
  btn1Text,
}) => {
  const [counter, setCounter] = useState("0h 0m 0s");

  useEffect(() => {
    if (startTimestampMS === "" || !open) return;
    const now = Date.now();

    // Find the distance between now and the count down date
    const timeElapsed = now - startTimestampMS;

    // Time calculations for days, hours, minutes and seconds
    var hours = Math.floor(
      (timeElapsed % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((timeElapsed % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeElapsed % (1000 * 60)) / 1000);

    // Display the result in the element with id="overlayTimer"
    const timeString = hours + "h " + minutes + "m " + seconds + "s";
    setTimeout(() => setCounter(timeString), 1000);
  }, [open, counter, startTimestampMS]);

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={open}
      onClick={handleClose}
    >
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1, width: "25ch" },
        }}
        noValidate
        autoComplete="off"
      >
        <Box sx={{ border: 1, borderRadius: 5 }}>
          <p>Start Computer Session?</p>
          <Typography variant="body1">{counter}</Typography>
          <Button
            variant="contained"
            onClick={() => {
              setOverlayResponse(true);
            }}
          >
            {btn1Text}
          </Button>
          <Button
            variant="contained"
            sx={{ backgroundColor: "#616161" }}
            onClick={() => {
              setOverlayResponse(false);
            }}
          >
            Cancel
          </Button>
        </Box>
      </Box>
    </Backdrop>
  );
};

export default Overlay;
