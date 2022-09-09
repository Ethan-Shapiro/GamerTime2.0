import React from "react";
import { Paper, Box, Button } from "@mui/material";

const ComputerButton = ({ onClickFunc }) => {
  return (
    <Paper elevation={15} sx={{ height: "7%", width: "7%" }}>
      <Button>
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
