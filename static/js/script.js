document.getElementById('routing-form').addEventListener('submit', function(e) {
    e.preventDefault();
  
    const startLocation = document.getElementById('start-location').value;
    const endLocation = document.getElementById('end-location').value;
    const containerType = document.getElementById('container-type').value;
    const containerQuantity = document.getElementById('container-quantity').value;
    const cargoWeight = document.getElementById('cargo-weight').value;
  
    fetch('/location?search=' + encodeURIComponent(startLocation))
      .then(response => response.json())
      .then(data => {
        const startLocationData = data[0];
  
        fetch('/location?search=' + encodeURIComponent(endLocation))
          .then(response => response.json())
          .then(data => {
            const endLocationData = data[0];
  
            const offerPayload = {
              cargoDetails: {
                container: {
                  amount: containerQuantity,
                  containerType: containerType,
                  cargoWeightPerContainer: cargoWeight,
                  unitOfMeasure: 'KG'
                },
                commodityGroup: {
                  name: 'FAK - Freight all Kind',
                  isHazardous: false
                }
              },
              endLocation: {
                name: endLocationData.name,
                locode: endLocationData.locode,
                haulage: 'CARRIERS_HAULAGE',
                postalCode: endLocationData.postalCode,
                businessLocode: endLocationData.businessLocode,
                country: endLocationData.country,
                continent: endLocationData.continent,
                locationType: endLocationData.locationType,
                portType: endLocationData.portType
              },
              startLocation: {
                name: startLocationData.name,
                locode: startLocationData.locode,
                haulage: 'CARRIERS_HAULAGE',
                businessLocode: startLocationData.businessLocode,
                country: startLocationData.country,
                continent: startLocationData.continent,
                locationType: startLocationData.locationType,
                portType: startLocationData.portType
              },
              validFrom: '2025-01-23T00:00:00+05:00'
            };
  
            fetch('/offers/offer', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(offerPayload)
            })
              .then(response => response.json())
              .then(data => {
                document.getElementById('result-container').classList.remove('hidden');
                document.getElementById('offer-details').textContent = JSON.stringify(data, null, 2);
              })
              .catch(error => {
                console.error('Error:', error);
              });
          })
          .catch(error => {
            console.error('Error:', error);
          });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });