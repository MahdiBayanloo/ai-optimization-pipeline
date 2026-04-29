# Scout Report — periCORE-SDK Blocking Call Discovery

**Generated:** 2026-04-22 15:53:27  
**SDK root:** /home/mahdi/pericore-sdk  
**Files scanned:** 85  
**Files skipped:** 211  
**Tokens:** 44311 in / 2062 out  

---

## Files Included in Scan

- `libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h`
- `libperiCORE/src/periCORE/implementation/update/FirmwareUpdate.h`
- `libperiCORE/src/periCORE/implementation/update/FirmwareUpdateTriggerFilter.h`
- `libperiCORE/src/periCORE/network/http/X509Endpoint.h`
- `libperiCORE/src/periCORE/implementation/update/FirmwareUpdateHeader.h`
- `libperiCORE/src/periCORE/api/security/certificates/FWSignCert.h`
- `libperiCORE/src/periCORE/hal/update/FirmwareImageSink.h`
- `libperiCORE/src/periCORE/implementation/network/HttpServer/CertificateGetEndpoint.h`
- `libperiCORE/src/periCORE/implementation/network/MQTTClient.h`
- `libperiCORE/src/periCORE/implementation/network/HttpServer.h`
- `libperiCORE/src/periCORE/implementation/network/CycloneTCPListener.h`
- `libperiCORE/src/periCORE/implementation/security/Service.h`
- `libperiCORE/src/periCORE/storage/impl/x509Endpoint.h`
- `libperiCORE/src/periCORE/network/http/Request.h`
- `libperiCORE/src/periCORE/network/mqtt/PublisherEndpoint.h`
- `libperiCORE/src/periCORE/implementation/network/HttpServer/EndpointManager.h`
- `libperiCORE/src/periCORE/implementation/deprecated/CertificateHandler.h`
- `libperiCORE/src/periCORE/api/security/ClientAuthMethod.h`
- `libperiCORE/src/periCORE/api/security/Level.h`
- `libperiCORE/src/periCORE/api/mqtt_client/State.h`
- `libperiCORE/src/periCORE/api/mqtt_client/Status.h`
- `libperiCORE/src/periCORE/network/http/Endpoint.h`
- `libperiCORE/src/periCORE/network/http/JSONEndpoint.h`
- `libperiCORE/src/periCORE/network/http/Response.h`
- `libperiCORE/src/periCORE/network/mqtt/Endpoint.h`
- `libperiCORE/src/periCORE/network/mqtt/SubscriberEndpoint.h`
- `libperiCORE/src/periCORE/network/mqtt/Topic.h`
- `libperiCORE/src/periCORE/lifecycle/UpdateStatus.h`
- `libperiCORE/src/periCORE/implementation/network/CycloneTCP.h`
- `libperiCORE/src/periCORE/implementation/lifecycle/FirmwareResetTimer.h`
- `libperiCORE/src/periCORE/implementation/lifecycle/FirmwareResetType.h`
- `libperiCORE/src/periCORE/implementation/update/TarHandler.h`
- `libperiCORE/src/periCORE/implementation/deprecated/CertificateReset.h`
- `libperiCORE/src/periCORE/implementation/deprecated/LegacySecurityAdapter.h`
- `libperiCORE/src/periCORE/node/FirmwareInfo.h`
- `libperiCORE/src/periCORE/security/InfoJSONEndpoint.h`
- `libperiCORE/src/periCORE/security/RoleJSONEndpoint.h`
- `libperiCORE/src/periCORE/security/UserRole.h`
- `libperiCORE/src/periCORE/api/mqtt/BrokerList.h`
- `libperiCORE/src/periCORE/api/security/Config.h`
- `libperiCORE/src/periCORE/api/security/Info.h`
- `libperiCORE/src/periCORE/api/security/SecurityAccessRole.h`
- `libperiCORE/src/periCORE/api/security/TrustAnchors.h`
- `libperiCORE/src/periCORE/api/mqtt_client/Config.h`
- `libperiCORE/src/periCORE/api/mqtt_client/Info.h`
- `libperiCORE/src/periCORE/storage/x509ConfigEndpoint.h`
- `libperiCORE/src/periCORE/storage/x509ProductionDataEndpoint.h`
- `libperiCORE/src/periCORE/storage/x509VolatileStorageEndpoint.h`
- `libperiCORE/src/perinet/periNODE/api/FwUpdate.h`
- `libperiCORE/src/perinet/periNODE/api/SecurityConfig.h`
- `applications/periNODE-0-10V-firmware/src/transformation/PolynomialTransformation.h`
- `applications/periNODE-0-10V-firmware/src/platform/ADS1115.h`
- `applications/periNODE-distance-firmware/src/platform/ADS1115.h`
- `applications/periNODE-distance-firmware/src/platform/UltraSonicSensor.h`
- `libperiCORE/src/periCORE/network/http/Method.h`
- `libperiCORE/src/periCORE/network/http/ResponseHeader.h`
- `libperiCORE/src/periCORE/network/http/ResponseStatus.h`
- `libperiCORE/src/periCORE/network/http/TriggerEndpoint.h`
- `libperiCORE/src/periCORE/implementation/network/HttpServer/WebInfoGetEndpoint.h`
- `applications/periNODE-0-10V-firmware/src/app/EventGenerator.h`
- `applications/periNODE-0-10V-firmware/src/app/SampleFilter.h`
- `applications/periNODE-0-10V-firmware/src/app/VoltageConverter.h`
- `applications/periNODE-0-10V-firmware/src/api/Adapter.h`
- `applications/periNODE-0-10V-firmware/src/api/Config.h`
- `applications/periNODE-0-10V-firmware/src/api/EventAdapter.h`
- `applications/periNODE-0-10V-firmware/src/api/EventConfig.h`
- `applications/periNODE-0-10V-firmware/src/api/EventGetAdapter.h`
- `applications/periNODE-0-10V-firmware/src/api/EventObject.h`
- `applications/periNODE-0-10V-firmware/src/api/ExtremeValues.h`
- `applications/periNODE-0-10V-firmware/src/api/Sample.h`
- `applications/periNODE-0-10V-firmware/src/api/Timestamp.h`
- `applications/periNODE-0-10V-firmware/src/api/TransformationConfig.h`
- `applications/periCORE-firmware/src/api/Config.h`
- `applications/periNODE-distance-firmware/src/platform/VoltageConverter.h`
- `applications/periNODE-distance-firmware/src/api/Adapter.h`
- `applications/periNODE-distance-firmware/src/api/Config.h`
- `applications/periNODE-distance-firmware/src/api/Sample.h`
- `applications/periCORE-firmware/src/api/GPIOSample.h`
- `applications/periCORE-firmware/src/api/RawDataSample.h`
- `applications/periCORE-firmware/src/peripherals/GPIOAdapter.h`
- `applications/periCORE-firmware/src/peripherals/I2CAdapter.h`
- `applications/periCORE-firmware/src/peripherals/UARTAdapter.h`
- `libperiCORE/src/periCORE/implementation/deprecated/config.h`
- `libperiCORE/src/periCORE/lifecycle/APIService.h`
- `libperiCORE/src/periCORE/lifecycle/FwStatus.h`

## Files Skipped

- `libperiCORE/src/periCORE/implementation/NodeEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/NodeEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/syscfg/partition_table.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/dnssd/Service.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/DMU.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/brphy_core_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/brphy_dsp_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/brphy_mii_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/brphy_misc_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/brphy_pll_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/gmac_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/io_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/p1588_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/qspi_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/tim_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/b1/uart_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/syscfg/mac_cfg.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/syscfg/xcvr_cfg.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/BCMFlashSink.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/EventChains.h` — context limit reached
- `libperiCORE/src/periCORE/node/Services.h` — context limit reached
- `libperiCORE/src/periCORE/hal/storage/PersistentMemory.h` — context limit reached
- `libperiCORE/src/periCORE/hal/storage/StorageManager.h` — context limit reached
- `libperiCORE/src/periCORE/dnssd/APIService.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/NodeConfig.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/NodeInfo.h` — context limit reached
- `seve/src/seve/lib/memory/AlignedStorage.h` — context limit reached
- `seve/src/seve/eventflow/SingleValue.h` — context limit reached
- `libperiCORE/src/magic_enum.hpp` — context limit reached
- `libperiCORE/src/periCORE/lifecycle/SoftResetTrigger.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/lib/crc32.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/network/MDNSResponder.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/lifecycle/RunStage.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/lifecycle/Service.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/I2CBB.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/QSPI.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/SPIBB.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/Switch.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_afe_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_br_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_cl45ven_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_core_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_dsp_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_mii_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_misc_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/rdb/c0/brphy_pll_rdb.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/Receiver.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gpio/InterruptGuardian.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/Flash.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/PartitionManager.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/KeyValueEncoder.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/WebUIDataStorage.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/dnssd/ServiceBuffer.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/Port.h` — context limit reached
- `libperiCORE/src/periCORE/node/APIService.h` — context limit reached
- `libperiCORE/src/periCORE/node/Info.h` — context limit reached
- `libperiCORE/src/periCORE/node/LifeState.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/GPIO.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/I2C.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/SPI.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/UART.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/spi/Descriptor.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/i2c/Descriptor.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/StringEndpoint.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/VersionInfo.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/types.h` — context limit reached
- `seve/unit-tests/platform_test.h` — context limit reached
- `seve/unit-tests/tpunit++.hpp` — context limit reached
- `seve/unit-tests/helper/HalProxy.h` — context limit reached
- `seve/unit-tests/helper/SystemAccessor_Helper.h` — context limit reached
- `seve/src/seve/InterruptHandler.h` — context limit reached
- `seve/src/seve/InterruptLock.h` — context limit reached
- `seve/src/seve/System.h` — context limit reached
- `seve/src/seve/SystemClock.h` — context limit reached
- `seve/src/seve/lib/Chain.h` — context limit reached
- `seve/src/seve/lib/Chainable.h` — context limit reached
- `seve/src/seve/lib/OStream.h` — context limit reached
- `seve/src/seve/lib/VirtualOneShotTimer.h` — context limit reached
- `seve/src/seve/lib/VirtualRepeatTimer.h` — context limit reached
- `seve/src/seve/lib/VirtualTimer.h` — context limit reached
- `seve/src/seve/lib/memory/Buffer.h` — context limit reached
- `seve/src/seve/lib/memory/BufferPool.h` — context limit reached
- `seve/src/seve/debug/DebugOStream.h` — context limit reached
- `seve/src/seve/debug/assert.h` — context limit reached
- `seve/src/seve/eventflow/EventDistributor.h` — context limit reached
- `seve/src/seve/eventflow/NoOpSink.h` — context limit reached
- `seve/src/seve/eventflow/Queue.h` — context limit reached
- `seve/src/seve/eventflow/Sink.h` — context limit reached
- `seve/src/seve/hal/hal.h` — context limit reached
- `seve/src/seve/scheduling/Activity.h` — context limit reached
- `seve/src/seve/scheduling/Scheduler.h` — context limit reached
- `seve/src/seve/scheduling/fifo/Activity.h` — context limit reached
- `seve/src/seve/scheduling/fifo/Scheduler.h` — context limit reached
- `seve/src/seve/scheduling/fifo/Scheduling.h` — context limit reached
- `libperiCORE/unit-tests/platform_test.h` — context limit reached
- `libperiCORE/unit-tests/tpunit++.hpp` — context limit reached
- `libperiCORE/unit-tests/helper/HalProxy.h` — context limit reached
- `libperiCORE/unit-tests/helper/SystemAccessor_Helper.h` — context limit reached
- `libperiCORE/unit-tests/helper/SystemClockFeeder.h` — context limit reached
- `libperiCORE/src/periCORE.h` — context limit reached
- `libperiCORE/src/seve/platform/armv6_m/InterruptGuardian.h` — context limit reached
- `libperiCORE/src/seve/platform/armv6_m/PowerManager.h` — context limit reached
- `libperiCORE/src/seve/platform/periCORE4/interrupts.h` — context limit reached
- `libperiCORE/src/periCORE/lib/BufferWriter.h` — context limit reached
- `libperiCORE/src/periCORE/lib/Fnv1a.h` — context limit reached
- `libperiCORE/src/periCORE/lib/JSONDeserializer.h` — context limit reached
- `libperiCORE/src/periCORE/lib/JSONSerializer.h` — context limit reached
- `libperiCORE/src/periCORE/lib/TarStreamReader.h` — context limit reached
- `libperiCORE/src/periCORE/lifecycle/Config.h` — context limit reached
- `libperiCORE/src/periCORE/lifecycle/Info.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/lib/memory.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/lifecycle/ProductionReset.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/node/NodeAttributes.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/node/Service.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/soc.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/GMAC.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/MDIO.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/PVT.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/UART.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/VectorNumbers.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/io.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/sysmap.h` — file too large
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/switchcore/MAC.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/switchcore/MDIPort.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/switchcore/RMIIPort.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/HardwareAdapter.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/MACFrameBuffer.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/MACFramePool.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/RxFrame.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gmac/Transmitter.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gpio/Gpio.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gpio/GpioBase.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89x4x/gpio/InterruptHandler.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/soc/bcm89241/soc.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/GPIO.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/NodeEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/PlatformEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/SystemCoreClock.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/WatchdogFeeder.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/crc.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/periCORE4.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/deprecated/PeriNODERuntimeAttributes.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/storage/ConfigurationStorage.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/storage/Flash.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/platform/periCORE4/storage/FlashDump.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/ConfigReset.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/LegacyNodeConfigAdapter.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/MessageWriter.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/PeriNODERuntimeAttributes.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/chunked.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/deprecated/compChunkedKeyValueDecoder.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/misc/Echo.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/misc/pvt/ApiAdapter.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/misc/pvt/Sample.h` — context limit reached
- `libperiCORE/src/periCORE/implementation/storage/EndpointManager.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/MDIPort.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/MIIPort.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/PortConfig.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/PortFlags.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/PortID.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/state/PhyStatus.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/stats/MDIPortStats.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/stats/MIIPortStats.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/stats/RXStats.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/stats/SQI.h` — context limit reached
- `libperiCORE/src/periCORE/switchcore/stats/TXStats.h` — context limit reached
- `libperiCORE/src/periCORE/node/Config.h` — context limit reached
- `libperiCORE/src/periCORE/node/ErrorStatus.h` — context limit reached
- `libperiCORE/src/periCORE/node/ProductionInfo.h` — context limit reached
- `libperiCORE/src/periCORE/platform/PlatformEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/platform/periCORE4/PlatformEnvironment.h` — context limit reached
- `libperiCORE/src/periCORE/platform/periCORE4/peripherals/gpio/Mapping.h` — context limit reached
- `libperiCORE/src/periCORE/hal/network/MAC.h` — context limit reached
- `libperiCORE/src/periCORE/hal/storage/KeyValueStorage.h` — context limit reached
- `libperiCORE/src/periCORE/hal/storage/MemoryTraits.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/MDIO.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/spi/Mode.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/spi/PinConfig.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/i2c/RegisterAccessDescr.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/uart/Baudrate.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/uart/Parity.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/uart/StopBits.h` — context limit reached
- `libperiCORE/src/periCORE/hal/peripherals/uart/WordLength.h` — context limit reached
- `libperiCORE/src/periCORE/storage/JSONConfigEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/JSONProductionDataEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/JSONVolatileStorageEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/MultipageStorage.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/ConfigEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/Endpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/JSONEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/NullStorageEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/storage/impl/ProductionDataEndpoint.h` — context limit reached
- `libperiCORE/src/periCORE/dnssd/Info.h` — context limit reached
- `libperiCORE/src/periCORE/dnssd/ServiceInfo.h` — context limit reached
- `libperiCORE/src/periCORE/dnssd/Services.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/InterfaceConfig.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/InterfaceSpecificConfig.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/InterfaceType.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/JSONDeserializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/JSONSerializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/KeyValueDeserializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/KeyValueSerializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/ProductionData.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/Sample.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/StreamWriter.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/StringDeserializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/StringSerializer.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/math.h` — context limit reached
- `libperiCORE/src/perinet/periNODE/api/tuples.h` — context limit reached
- `seve/src/seve/lib/memory/AtomicStorage.h` — context limit reached
- `seve/src/seve/eventflow/CountingTrigger.h` — context limit reached

---

## Analysis

# Static Analysis Report: Blocking Call Detection

## Findings

### Finding 1
- **FILE:** libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h
- **FUNCTION:** httpServerEstablishSecureConnection (declaration)
- **LINE HINT:** `error_t httpServerEstablishSecureConnection(HttpConnection *connection);`
- **BLOCKING TYPE:** TLS handshake
- **SEVERITY:** HIGH
- **NOTE:** CycloneTCP's TLS connection establishment is synchronous and performs the full TLS handshake which involves multiple network round-trips and crypto operations.

### Finding 2
- **FILE:** libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h
- **FUNCTION:** httpServerOpenSecureConnection (declaration)
- **LINE HINT:** `error_t httpServerOpenSecureConnection(HttpServerContext *context, HttpConnection *connection);`
- **BLOCKING TYPE:** TLS handshake
- **SEVERITY:** HIGH
- **NOTE:** Opening a secure connection in CycloneTCP involves TLS context initialization and potentially blocking socket operations.

### Finding 3
- **FILE:** libperiCORE/src/periCORE/implementation/network/MQTTClient.h
- **FUNCTION:** mqttClientStateConnect
- **LINE HINT:** `void mqttClientStateConnect(void);`
- **BLOCKING TYPE:** TLS handshake / sync socket
- **SEVERITY:** HIGH
- **NOTE:** MQTT client connection state involves TLS handshake via mqttTlsInitCallback and CycloneTCP's blocking MQTT connect which performs socket connection and TLS establishment.

### Finding 4
- **FILE:** libperiCORE/src/periCORE/implementation/network/MQTTClient.h
- **FUNCTION:** mqttTlsInitCallback (static callback)
- **LINE HINT:** `static error_t mqttTlsInitCallback(MqttClientContext* context, TlsContext* tlsContext);`
- **BLOCKING TYPE:** TLS handshake / crypto
- **SEVERITY:** HIGH
- **NOTE:** TLS initialization callback is invoked during MQTT connection and involves certificate loading and TLS context setup which can block.

### Finding 5
- **FILE:** libperiCORE/src/periCORE/implementation/network/MQTTClient.h
- **FUNCTION:** mqtt_cert_verification_callback (static callback)
- **LINE HINT:** `static error_t mqtt_cert_verification_callback(TlsContext *, const X509CertificateInfo *, uint_t, void *);`
- **BLOCKING TYPE:** crypto
- **SEVERITY:** MEDIUM
- **NOTE:** Certificate verification callback processes X509CertificateInfo which may involve cryptographic signature verification operations.

### Finding 6
- **FILE:** libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h
- **FUNCTION:** httpServerUserCertificateCallback
- **LINE HINT:** `error_t httpServerUserCertificateCallback(TlsContext *tlsContext, const X509CertificateInfo *certInfo, uint_t pathLen, void *param);`
- **BLOCKING TYPE:** crypto
- **SEVERITY:** MEDIUM
- **NOTE:** User certificate callback processes X509CertificateInfo for mTLS which involves certificate chain validation and potential crypto operations.

### Finding 7
- **FILE:** libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h
- **FUNCTION:** httpServerSendData
- **LINE HINT:** `error_t httpServerSendData(HttpConnection *connection, const void *data, size_t length, size_t *written, uint_t flags);`
- **BLOCKING TYPE:** sync socket
- **SEVERITY:** MEDIUM
- **NOTE:** CycloneTCP socket send operations may block waiting for the TCP transmit buffer to have space, depending on implementation and flags.

### Finding 8
- **FILE:** libperiCORE/src/periCORE/implementation/network/HttpServer/ConnectionHelper.h
- **FUNCTION:** httpServerReceiveData
- **LINE HINT:** `error_t httpServerReceiveData(HttpConnection *connection, void *data, size_t size, size_t *received, uint_t flags);`
- **BLOCKING TYPE:** sync socket
- **SEVERITY:** MEDIUM
- **NOTE:** CycloneTCP socket receive operations may block waiting for data depending on socket configuration and flags passed.

### Finding 9
- **FILE:** libperiCORE/src/periCORE/implementation/update/FirmwareUpdate.h
- **FUNCTION:** verify_header_integrity
- **LINE HINT:** `bool verify_header_integrity(std::string_view signature,std::string_view header);`
- **BLOCKING TYPE:** crypto
- **SEVERITY:** MEDIUM
- **NOTE:** Signature verification likely uses ECDSA operations (ecdsa.h is included) which involve computationally intensive elliptic curve math.

### Finding 10
- **FILE:** libperiCORE/src/periCORE/implementation/update/FirmwareUpdate.h
- **FUNCTION:** verify_image_integrity
- **LINE HINT:** `bool verify_image_integrity(Sha256Context& calculated,const uint8_t* image);`
- **BLOCKING TYPE:** crypto
- **SEVERITY:** LOW
- **NOTE:** SHA256 digest comparison is fast but if this function also includes signature verification of the digest, it could involve blocking ECDSA operations.

### Finding 11
- **FILE:** libperiCORE/src/periCORE/implementation/network/MQTTClient.h
- **FUNCTION:** mqttClientStateResolve
- **LINE HINT:** `void mqttClientStateResolve(void);`
- **BLOCKING TYPE:** sync socket
- **SEVERITY:** MEDIUM
- **NOTE:** DNS resolution in CycloneTCP can be synchronous, blocking while waiting for DNS response from network.

### Finding 12
- **FILE:** libperiCORE/src/periCORE/implementation/network/MQTTClient.h
- **FUNCTION:** mqttClientStateResolveAppName
- **LINE HINT:** `void mqttClientStateResolveAppName(void);`
- **BLOCKING TYPE:** sync socket
- **SEVERITY:** MEDIUM
- **NOTE:** Application name resolution likely involves mDNS/DNS lookup which can block waiting for network response.

### Finding 13
- **FILE:** libperiCORE/src/periCORE/implementation/network/CycloneTCPListener.h
- **FUNCTION:** CycloneTCPListenerImpl::run
- **LINE HINT:** `virtual void run() override;`
- **BLOCKING TYPE:** sync socket
- **SEVERITY:** MEDIUM
- **NOTE:** TCP listener run method likely calls CycloneTCP accept() or similar socket operations which may block if not configured for non-blocking mode.

---

## SUMMARY

| Severity | Count |
|----------|-------|
| **HIGH** | 4 |
| **MEDIUM** | 8 |
| **LOW** | 1 |
| **Total** | 13 |

### Recommended First Target
**`httpServerEstablishSecureConnection`** in `ConnectionHelper.h`

This is the most isolated HIGH-severity finding because:
1. It's a single function with a clear, well-defined purpose (TLS handshake)
2. It's already abstracted as a helper function, making it easier to replace
3. The HTTP server connection state machine (evidenced by `httpServerChangeState`) suggests existing state infrastructure to build upon
4. It affects the HTTP server which is central to the system's functionality

### Recommended Transformation Pattern
**State Machine**

The codebase already shows state machine patterns:
- `HttpConnState` and `httpServerChangeState` in the HTTP server
- `MQTT_States` and `mqttClientChangeState` in the MQTT client
- The event-driven architecture with `seve::eventflow` queues and sinks

The TLS handshake should be decomposed into discrete states (e.g., `TLS_STATE_CLIENT_HELLO_SENT`, `TLS_STATE_WAITING_SERVER_HELLO`, `TLS_STATE_KEY_EXCHANGE`, etc.) that yield control back to the event loop between each network I/O operation. CycloneTCP may support non-blocking TLS operations that can be polled, allowing the state machine to check for completion and progress through handshake stages incrementally.

---

## Next Step

Review the HIGH findings above. For each target:
1. `cp -r task_template/ task_<name>/`
2. Update `knowledge/system_summary.md` for periCORE-SDK
3. Write `tasks/task.md` naming the specific file and function
4. Copy the target source file into `codebase/`
5. `python3 run_pipeline.py --task task_<name>/`