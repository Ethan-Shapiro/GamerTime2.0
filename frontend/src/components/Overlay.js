import React, { useEffect, useState } from "react";
import { Backdrop, Box, Button, Typography } from "@mui/material";

const Overlay = ({ open, setOpen, setOverlayResponse, btn1Text, counter }) => {
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
