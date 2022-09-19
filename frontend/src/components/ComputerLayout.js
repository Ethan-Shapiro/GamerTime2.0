import React, { useEffect, useState } from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerButton from "./ComputerButton";
import axios from "axios";

const ComputerLayout = () => {
  const [initialData, setInitialData] = useState({});
  useEffect(() => {
    axios
      .get(`http://localhost:5050/openrec/`, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        }})
      .then((response) => {
        const data = response.data;
        const initDataDict = {};
        for (let i = 0; i < data.length; i++) {
          initDataDict[data[i]["id"]] = data[i];
        }
        console.log(initDataDict);
        setInitialData(initDataDict);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  }, []);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container rowSpacing={3} columnSpacing={1}>
        <Grid xs={12}>
          <Grid container rowSpacing={1} columns={8}>
            {Array.apply(null, Array(12)).map((x, i) => {
              if (i + 1 === 2 || i + 1 === 8) {
                return (
                  <Grid key={i} xsOffset={2} xs={1}>
                    <ComputerButton
                      ID={i + 1}
                      initData={
                        i + 1 in initialData ? initialData[i + 1] : null
                      }
                    ></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid key={i} xs={1}>
                    <ComputerButton
                      ID={i + 1}
                      initData={
                        i + 1 in initialData ? initialData[i + 1] : null
                      }
                    ></ComputerButton>
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
                  <Grid key={i} xsOffset={1} xs={1}>
                    <ComputerButton
                      ID={i + 1 + 12}
                      initData={
                        i + 1 + 12 in initialData
                          ? initialData[i + 1 + 12]
                          : null
                      }
                    ></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid key={i} xs={1}>
                    <ComputerButton
                      ID={i + 1 + 12}
                      initData={
                        i + 1 + 12 in initialData
                          ? initialData[i + 1 + 12]
                          : null
                      }
                    ></ComputerButton>
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
