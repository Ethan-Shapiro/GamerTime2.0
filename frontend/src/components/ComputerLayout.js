import React, { useEffect, useState } from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerButton from "./ComputerButton";
import axios from "axios";

const ComputerLayout = ({
  setCompStatusChange,
  addMessage,
  getAccessToken,
}) => {
  const [initialData, setInitialData] = useState({});

  useEffect(() => {
    getAccessToken().then((accessToken) => {
      axios
        .get(`/api/openrec/`, {
          headers: {
            Authorization: accessToken,
          },
        })
        .then((response) => {
          const data = response.data;
          console.log(data);

          setInitialData(data);
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
          }
        });
    });
  }, []);

  const compNameDict = {
    1: "E1",
    2: "A1",
    3: "A2",
    4: "A3",
    5: "A4",
    6: "A5",
    7: "E2",
    8: "B1",
    9: "B2",
    10: "B3",
    11: "B4",
    12: "B5",
    13: "E3",
    14: "C1",
    15: "C2",
    16: "C3",
    17: "C4",
    18: "C5",
    19: "C6",
    20: "E4",
    21: "D1",
    22: "D2",
    23: "D3",
    24: "D4",
    25: "D5",
    26: "D6",
  };

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
                      Name={compNameDict[i + 1]}
                      setCompStatusChange={setCompStatusChange}
                      addMessage={addMessage}
                      initData={
                        i + 1 in initialData ? initialData[i + 1] : null
                      }
                      getAccessToken={getAccessToken}
                    ></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid key={i} xs={1}>
                    <ComputerButton
                      ID={i + 1}
                      Name={compNameDict[i + 1]}
                      setCompStatusChange={setCompStatusChange}
                      addMessage={addMessage}
                      initData={
                        i + 1 in initialData ? initialData[i + 1] : null
                      }
                      getAccessToken={getAccessToken}
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
                      Name={compNameDict[i + 1 + 12]}
                      setCompStatusChange={setCompStatusChange}
                      addMessage={addMessage}
                      initData={
                        i + 1 + 12 in initialData
                          ? initialData[i + 1 + 12]
                          : null
                      }
                      getAccessToken={getAccessToken}
                    ></ComputerButton>
                  </Grid>
                );
              } else {
                return (
                  <Grid key={i} xs={1}>
                    <ComputerButton
                      ID={i + 1 + 12}
                      Name={compNameDict[i + 1 + 12]}
                      setCompStatusChange={setCompStatusChange}
                      addMessage={addMessage}
                      initData={
                        i + 1 + 12 in initialData
                          ? initialData[i + 1 + 12]
                          : null
                      }
                      getAccessToken={getAccessToken}
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
