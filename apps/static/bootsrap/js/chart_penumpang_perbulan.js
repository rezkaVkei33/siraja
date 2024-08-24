document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/penumpang-perbulan/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Pastikan data tidak null atau undefined
            const bulanLabels = data.bulan_labels || [];
            const jumlahNaik = data.jumlah_naik || [];
            const jumlahTurun = data.jumlah_turun || [];

            // Pastikan elemen 'penumpangPerBulanChart' ada di halaman
            const ctxElement = document.getElementById('penumpangPerBulanChart');
            if (ctxElement) {
                const ctx = ctxElement.getContext('2d');

                const penumpangPerBulanChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: bulanLabels,
                        datasets: [
                            {
                                label: 'Jumlah Naik',
                                backgroundColor: '#b1c81c',
                                data: jumlahNaik,
                            },
                            {
                                label: 'Jumlah Turun',
                                backgroundColor: '#1c30c8',
                                data: jumlahTurun,
                            }
                        ],
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            } else {
                console.error("Element 'penumpangPerBulanChart' tidak ditemukan di halaman.");
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});
