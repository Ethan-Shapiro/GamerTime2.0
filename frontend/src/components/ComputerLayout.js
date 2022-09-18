import React, { useEffect } from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerButton from "./ComputerButton";
import axios from "axios";

const ComputerLayout = () => {
  useEffect(() => {
    axios
      .get(`http://localhost:5050/openrec/`)
      .then((response) => {
        const data = response.data;
        console.log(data);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  });

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container rowSpacing={3} columnSpacing={1}>
        <Grid xs={12}>
          <Grid container rowSpacing={1} columns={8}>
            {Array.apply(null, Array(12)).map((x, i) => {
              if (i + 1 === 2 || i + 1 === 8) {
                return (
                  <Grid xsOffset={2} xs={1}>
                    <ComputerButton ID={i + 1}></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid xs={1}>
                    <ComputerButton ID={i + 1}></ComputerButton>
                  </Grid>
                );
              }
            })}
          </Grid>
        </Grid>
        <Grid xs={12}>
          <Grid container rowSpacing={1} columns={8}>
            {Array.apply(null, Array(14)).map((x, i) => {
              if (i + 1 === 2 || i + 1 === 9) {
                return (
                  <Grid xsOffset={1} xs={1}>
                    <ComputerButton ID={i + 1 + 12}></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid xs={1}>
                    <ComputerButton ID={i + 1 + 12}></ComputerButton>
                  </Grid>
                );
              }
            })}
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ComputerLayout;
